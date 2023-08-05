import argparse
import boto3
import botocore

from botocore.config import Config
import click
import datetime
import json
import logging
import os
import sys
import tabulate
import time
from typing import Any, Dict, List, Optional
import uuid


import ray.projects.scripts as ray_scripts
import ray.ray_constants

import anyscale.conf
from anyscale.autosync import AutosyncRunner
from anyscale.project import PROJECT_ID_BASENAME, get_project_id, load_project_or_throw
from anyscale.snapshot import (
    copy_file,
    create_snapshot,
    delete_snapshot,
    describe_snapshot,
    download_snapshot,
    get_snapshot_uuid,
    list_snapshots,
)
from anyscale.util import (
    confirm,
    deserialize_datetime,
    execution_log_name,
    get_cluster_config,
    get_available_regions,
    _get_role,
    _get_user,
    _resource,
    humanize_timestamp,
    send_json_request,
)
from anyscale.auth_proxy import app as auth_proxy_app


logging.basicConfig(format=ray.ray_constants.LOGGER_FORMAT)
logger = logging.getLogger(__file__)
logging.getLogger("botocore").setLevel(logging.CRITICAL)

if anyscale.conf.AWS_PROFILE is not None:
    logger.info("Using AWS profile %s", anyscale.conf.AWS_PROFILE)
    os.environ["AWS_PROFILE"] = anyscale.conf.AWS_PROFILE


def get_or_create_snapshot(
    snapshot_uuid: Optional[str], description: str, project_definition: Any, yes: bool
) -> str:
    # If no snapshot was provided, create a snapshot.
    if snapshot_uuid is None:
        confirm("No snapshot specified for the command. Create a new snapshot?", yes)
        snapshot_uuid = create_snapshot(
            project_definition,
            yes,
            description=description,
            tags=["anyscale:session_startup"],
        )
    else:
        snapshot_uuid = get_snapshot_uuid(project_definition.root, snapshot_uuid)
    return snapshot_uuid


@click.group()
def cli() -> None:
    pass


@click.group("project", help="Commands for working with projects.")
def project_cli() -> None:
    pass


@click.group("session", help="Commands for working with sessions.")
def session_cli() -> None:
    pass


@click.group("snapshot", help="Commands for working with snapshot.")
def snapshot_cli() -> None:
    pass


@click.group("aws", help="Commands for setting up credentials with cloud providers")
def aws_cli() -> None:
    pass


@click.command(name="version", help="Show version of anyscale.")
def version_cli() -> None:
    print(anyscale.__version__)


def setup_cross_account_role(email: str, region: str) -> None:

    response = send_json_request("user_aws_get_anyscale_account", {})
    assert "anyscale_aws_account" in response

    anyscale_aws_account = response["anyscale_aws_account"]
    anyscale_aws_iam_role_policy = {
        "Version": "2012-10-17",
        "Statement": {
            "Sid": "1",
            "Effect": "Allow",
            "Principal": {"AWS": anyscale_aws_account},
            "Action": "sts:AssumeRole",
        },
    }

    AWS_IAM_ANYSCALE_ROLE_NAME = f"anyscale-iam-role-{str(uuid.uuid4())[:8]}"

    iam = _resource("iam", region)

    role = _get_role(AWS_IAM_ANYSCALE_ROLE_NAME, region)
    if role is None:
        iam.create_role(
            RoleName=AWS_IAM_ANYSCALE_ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(anyscale_aws_iam_role_policy),
        )
        role = _get_role(AWS_IAM_ANYSCALE_ROLE_NAME, region)

    assert role is not None, "Failed to create IAM role!"

    role.attach_policy(PolicyArn="arn:aws:iam::aws:policy/AmazonEC2FullAccess")
    role.attach_policy(PolicyArn="arn:aws:iam::aws:policy/IAMFullAccess")

    print(f"Created IAM role {role.arn}")

    send_json_request(
        "user_setup_aws_cross_account_role",
        {"email": email, "user_iam_role_arn": role.arn, "region": region},
        post=True,
    )


@aws_cli.command(
    name="setup",
    help="Set up aws credentials. By default, This creates an IAM role in your account that will"
    "later be assumed by anyscale account.",
)
@click.option(
    "--region", help="Region to set up the credentials in.", default="us-west-2"
)
def setup_aws(region: str) -> None:

    os.environ["AWS_DEFAULT_REGION"] = region
    regions_available = get_available_regions()
    if region not in regions_available:
        raise click.ClickException(
            f"Region '{region}' is not available. Regions availables are {regions_available}"
        )

    confirm(
        "\nYou are about to give anyscale full access to EC2 and IAM in your account.\n\n"
        "Continue?",
        False,
    )

    response = send_json_request("user_info", {})
    email = response["email"]

    setup_cross_account_role(email, region)

    # Sleep for 5 seconds to make sure the policies take effect.
    time.sleep(5)

    print("AWS credentials setup complete!")
    print(
        "You can revoke the access at any time by deleting anyscale IAM user/role in your account."
    )
    print("Head over to the web UI to create new sessions in your AWS account!")


@project_cli.command(name="validate", help="Validate current project specification.")
@click.option("--verbose", help="If set, print the validated file", is_flag=True)
def project_validate(verbose: bool) -> None:
    project = load_project_or_throw()
    print("Project files validated!", file=sys.stderr)
    if verbose:
        print(project.config)


def register_project(project_definition: Any) -> None:
    project_id_path = os.path.join(ray_scripts.PROJECT_DIR, PROJECT_ID_BASENAME)

    project_name = project_definition.config["name"]
    description = project_definition.config.get("description", "")
    # Add a description of the output_files parameter to the project yaml.
    if "output_files" not in project_definition.config:
        with open(ray_scripts.PROJECT_YAML, "a") as f:
            f.write(
                "\n".join(
                    [
                        "",
                        "# Pathnames for files and directories that should be saved",
                        "# in a snapshot but that should not be synced with a"
                        "# session. Pathnames can be relative to the project",
                        "# directory or absolute. Generally, this should be files",
                        "# that were created by an active session, such as",
                        "# application checkpoints and logs.",
                        "output_files: [",
                        "  # For example, uncomment this to save the logs from the",
                        "  # last ray job.",
                        '  # "/tmp/ray/session_latest",',
                        "]",
                    ]
                )
            )

    if os.path.exists(project_id_path):
        with open(project_id_path, "r") as f:
            project_id = int(f.read())
        resp = send_json_request("project_list", {"project_id": project_id})
        if len(resp["projects"]) == 0:
            raise click.ClickException(
                "This project has already been "
                "registered, but its database entry has been deleted?"
            )
        elif len(resp["projects"]) > 1:
            raise click.ClickException("Multiple projects found with the same ID.")

        project = resp["projects"][0]
        if project_name != project["name"]:
            raise ValueError(
                "Project name {} does not match saved project name "
                "{}".format(project_name, project["name"])
            )

        raise click.ClickException("This project has already been registered")

    # Add a database entry for the new Project.
    resp = send_json_request(
        "project_create",
        {"project_name": project_name, "description": description},
        post=True,
    )
    project_id = resp["project_id"]
    with open(project_id_path, "w+") as f:
        f.write(str(project_id))

    # Create initial snapshot for the project.
    try:
        create_snapshot(
            project_definition,
            False,
            description="Initial project snapshot",
            tags=["anyscale:initial"],
        )
    except click.Abort as e:
        raise e
    except Exception as e:
        # Creating a snapshot can fail if the project is not found or if some
        # files cannot be copied (e.g., due to permissions).
        raise click.ClickException(e)  # type: ignore


@project_cli.command(
    name="register", help="Register an existing project within current directory."
)
@click.pass_context
def project_register(ctx: Any) -> None:
    send_json_request("user_info", {})

    if not os.path.exists(ray_scripts.PROJECT_DIR):
        raise click.ClickException(
            "No registered project found. Did you "
            "mean to call `anyscale project create <project_name>`?"
        )

    try:
        project_definition = load_project_or_throw()
    except click.ClickException as e:
        raise e
    register_project(project_definition)


@project_cli.command(
    name="create", help="Create a new project within current directory."
)
@click.argument("project_name", required=True)
@click.option(
    "--cluster-yaml", help="Path to autoscaler yaml. Created by default", default=None
)
@click.option(
    "--requirements", help="Path to requirements.txt. Created by default", default=None
)
@click.pass_context
def project_create(
    ctx: Any,
    project_name: str,
    cluster_yaml: Optional[str],
    requirements: Optional[str],
) -> None:
    # Send an initial request to the server to make sure we are actually
    # registered. We only want to create the project if that is the case,
    # to avoid projects that are created but not registered.
    send_json_request("user_info", {})
    ctx.forward(ray_scripts.create)

    try:
        project_definition = load_project_or_throw()
    except click.ClickException as e:
        raise e
    register_project(project_definition)


@project_cli.command(name="list", help="List all projects currently registered.")
@click.pass_context
def project_list(ctx: Any) -> None:
    resp = send_json_request("project_list", {})
    project_table = []
    print("Projects:")
    for project in resp["projects"]:
        project_table.append(
            [
                project["name"],
                "{}/project/{}".format(
                    anyscale.conf.ANYSCALE_PRODUCTION_NAME, project["id"]
                ),
                project["description"],
            ]
        )
    print(
        tabulate.tabulate(
            project_table, headers=["NAME", "URL", "DESCRIPTION"], tablefmt="plain"
        )
    )


def remote_snapshot(
    project_id: int,
    session_name: str,
    additional_files: List[str],
    files_only: bool = False,
) -> str:
    resp = send_json_request(
        "project_sessions", {"project_id": project_id, "session_name": session_name}
    )
    sessions = resp["sessions"]

    if len(sessions) != 1:
        raise click.ClickException(
            "Session matching pattern {} not unique".format(session_name)
        )

    session = sessions[0]

    resp = send_json_request(
        "session_snapshot",
        {
            "session_id": session["id"],
            "additional_files": additional_files,
            "files_only": files_only,
        },
        post=True,
    )
    if "snapshot_uuid" not in resp:
        raise click.ClickException(
            "Snapshot creation of session {} failed!".format(session_name)
        )
    snapshot_uuid: str = resp["snapshot_uuid"]
    return snapshot_uuid


@snapshot_cli.command(name="create", help="Create a snapshot of the current project.")
@click.argument(
    "files", nargs=-1, required=False,
)
@click.option("--description", help="A description of the snapshot", default=None)
@click.option(
    "--session-name",
    help="If specified, a snapshot of the remote session"
    "with that name will be taken.",
    default=None,
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
@click.option(
    "--include-output-files",
    is_flag=True,
    default=False,
    help="Include output files with the snapshot",
)
@click.option(
    "--files-only",
    is_flag=True,
    default=False,
    help="If specified, files in the project directory are not included in the snapshot",
)
@click.option(
    "--tag",
    type=str,
    help="Tag for this snapshot. Multiple tags can be specified by repeating this option.",
    multiple=True,
)
def snapshot_create(
    files: List[str],
    description: Optional[str],
    session_name: Optional[str],
    yes: bool,
    include_output_files: bool,
    files_only: bool,
    tag: List[str],
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    files = list(files)
    if len(files) > 0:
        files = [os.path.abspath(f) for f in files]

    if session_name:
        # Create a remote snapshot.
        try:
            snapshot_uuid = remote_snapshot(project_id, session_name, files, files_only)
            print(
                "Snapshot {snapshot_uuid} of session {session_name} created!".format(
                    snapshot_uuid=snapshot_uuid, session_name=session_name
                )
            )
        except click.ClickException as e:
            raise e

    else:
        # Create a local snapshot.
        try:
            create_snapshot(
                project_definition,
                yes,
                description=description,
                include_output_files=include_output_files,
                additional_files=files,
                files_only=files_only,
                tags=tag,
            )
        except click.Abort as e:
            raise e
        except Exception as e:
            # Creating a snapshot can fail if the project is not found or
            # if some files cannot be copied (e.g., due to permissions).
            raise click.ClickException(e)  # type: ignore


@snapshot_cli.command(
    name="delete", help="Delete a snapshot of the current project with the given UUID."
)
@click.argument("uuid")
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
def snapshot_delete(uuid: str, yes: bool) -> None:
    project_definition = load_project_or_throw()
    try:
        delete_snapshot(project_definition.root, uuid, yes)
    except click.Abort as e:
        raise e
    except Exception as e:
        # Deleting a snapshot can fail if the project is not found.
        raise click.ClickException(e)  # type: ignore


@snapshot_cli.command(name="list", help="List all snapshots of the current project.")
def snapshot_list() -> None:
    project_definition = load_project_or_throw()

    try:
        snapshots = list_snapshots(project_definition.root)
    except Exception as e:
        # Listing snapshots can fail if the project is not found.
        raise click.ClickException(e)  # type: ignore

    if len(snapshots) == 0:
        print("No snapshots found.")
    else:
        print("Project snaphots:")
        for snapshot in snapshots:
            print(" {}".format(snapshot))


@snapshot_cli.command(
    name="describe", help="Describe metadata and files of a snapshot."
)
@click.argument("name")
def snapshot_describe(name: str) -> None:
    try:
        description = describe_snapshot(name)
    except Exception as e:
        # Describing a snapshot can fail if the snapshot does not exist.
        raise click.ClickException(e)  # type: ignore

    print(description)


@snapshot_cli.command(name="download", help="Download a snapshot.")
@click.argument("name")
@click.option("--target-directory", help="Directory this snapshot is downloaded to.")
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="If set, the downloaded snapshot will overwrite existing directory",
)
def snapshot_download(
    name: str, target_directory: Optional[str], overwrite: bool
) -> None:
    try:
        resp = send_json_request("user_get_temporary_aws_credentials", {})
    except Exception as e:
        # The snapshot may not exist.
        raise click.ClickException(e)  # type: ignore

    assert "AWS_ACCESS_KEY_ID" in resp["credentials"]

    download_snapshot(
        name,
        resp["credentials"],
        target_directory=target_directory,
        overwrite=overwrite,
    )


@snapshot_cli.command(name="pull", help="Pull files from a session")
@click.argument("session_name", required=True)
@click.argument("files", type=click.Path(), nargs=-1)
@click.option(
    "--include-output-files",
    is_flag=True,
    default=False,
    help="Download output files as well",
)
@click.option("--target-directory", help="Directory the files are downloaded to.")
def snapshot_pull(
    session_name: str,
    files: List[str],
    include_output_files: bool,
    target_directory: str,
) -> None:
    if not files:
        raise click.ClickException("Nothing to pull!")

    project_definition = load_project_or_throw()
    project_dir = project_definition.root
    if not target_directory:
        target_directory = project_dir

    target_directory = os.path.abspath(target_directory)

    try:
        print("Collecting files from remote.")
        project_id = get_project_id(project_definition.root)
        snapshot_id = remote_snapshot(project_id, session_name, files, files_only=True)
        resp = send_json_request("user_get_temporary_aws_credentials", {})
        print("Downloading files.")
        download_snapshot(snapshot_id, resp["credentials"], target_directory)
    except Exception as e:
        raise click.ClickException(e)  # type: ignore


@session_cli.command(name="attach", help="Open a console for the given session.")
@click.option("--name", help="Name of the session to open a console for.", default=None)
@click.option("--tmux", help="Attach console to tmux.", is_flag=True)
@click.option("--screen", help="Attach console to screen.", is_flag=True)
def session_attach(name: Optional[str], tmux: bool, screen: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    resp = send_json_request(
        "project_sessions", {"project_id": project_id, "session_name": name}
    )
    sessions = resp["sessions"]

    if len(sessions) != 1:
        raise click.ClickException(
            "Multiple ({}) sessions found with name {}".format(len(sessions), name)
        )

    session = sessions[0]
    ray.autoscaler.commands.attach_cluster(
        project_definition.cluster_yaml(),
        start=False,
        use_tmux=tmux,
        use_screen=screen,
        override_cluster_name=session["name"],
        new=False,
    )


@session_cli.command(
    name="commands", help="Print available commands for sessions of this project."
)
def session_commands() -> None:
    project_definition = load_project_or_throw()
    print("Active project: " + project_definition.config["name"])
    print()

    commands = project_definition.config["commands"]

    for command in commands:
        print('Command "{}":'.format(command["name"]))
        parser = argparse.ArgumentParser(
            command["name"], description=command.get("help"), add_help=False
        )
        params = command.get("params", [])
        for param in params:
            name = param.pop("name")
            if "type" in param:
                param.pop("type")
            parser.add_argument("--" + name, **param)
        help_string = parser.format_help()
        # Indent the help message by two spaces and print it.
        print("\n".join(["  " + line for line in help_string.split("\n")]))


@session_cli.command(
    name="start",
    context_settings=dict(ignore_unknown_options=True,),
    help="Start a session based on the current project configuration.",
)
# TODO(pcm): Change this to be
# anyscale session start --arg1=1 --arg2=2 command args
# instead of
# anyscale session start --session-args=--arg1=1,--arg2=2 command args
@click.option(
    "--session-args",
    help="Arguments that get substituted into the cluster config "
    "in the format --arg1=1,--arg2=2",
    default="",
)
@click.argument("command_name", required=False)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "--shell",
    help="If set, run the command as a raw shell command instead "
    "of looking up the command in the project.yaml.",
    is_flag=True,
)
@click.option(
    "--snapshot",
    help="If set, start the session from the given snapshot.",
    default=None,
)
@click.option("--name", help="A name to tag the session with.", default=None)
def session_start(
    session_args: str,
    command_name: Optional[str],
    args: List[str],
    shell: bool,
    snapshot: Optional[str],
    name: Optional[str],
) -> None:
    # TODO(pcm): Remove the dependence of the product on Ray.
    from ray.projects.projects import make_argument_parser

    project_definition = load_project_or_throw()
    if not name:
        name = project_definition.config["name"]
    # Parse the session arguments.
    cluster_params = project_definition.config["cluster"].get("params")
    if cluster_params:
        parser, choices = make_argument_parser("session params", cluster_params, False)
        session_params = vars(parser.parse_args(session_args.split(",")))
    else:
        session_params = {}
    # Get the shell command to run. This also validates the command,
    # which should be done before the cluster is started.
    try:
        (shell_command, parsed_args, config) = project_definition.get_command_info(
            command_name, args, shell, wildcards=True
        )
    except ValueError as e:
        raise click.ClickException(e)  # type: ignore
    if command_name and shell:
        command_name = " ".join([command_name] + list(args))
    session_runs = ray_scripts.get_session_runs(name, command_name, parsed_args)

    assert len(session_runs) == 1, "Running sessions with a wildcard is deprecated"
    session_run = session_runs[0]

    project_id = get_project_id(project_definition.root)
    snapshot_uuid = get_or_create_snapshot(
        snapshot,
        description="Initial snapshot for session {}".format(session_run["name"]),
        project_definition=project_definition,
        yes=True,
    )

    session_name = session_run["name"]
    resp = send_json_request(
        "session_list",
        {"project_id": project_id, "session_name": session_name, "active_only": False},
    )
    if len(resp["sessions"]) == 0:
        resp = send_json_request(
            "session_create",
            {
                "project_id": project_id,
                "session_name": session_name,
                "snapshot_uuid": snapshot_uuid,
                "session_params": session_params,
                "command_name": command_name,
                "command_params": session_run["params"],
                "shell": shell,
            },
            post=True,
        )
    elif len(resp["sessions"]) == 1:
        if session_params != {}:
            raise click.ClickException(
                "Session parameters are not supported when restarting a session"
            )
        send_json_request(
            "session_start", {"session_id": resp["sessions"][0]["id"]}, post=True
        )
    else:
        raise click.ClickException(
            "Multiple sessions with name {} exist".format(session_name)
        )


@session_cli.command(name="sync", help="Synchronize a session with a snapshot.")
@click.option(
    "--snapshot",
    help="The snapshot UUID the session should be synchronized with.",
    default=None,
)
@click.option("--name", help="The name of the session to synchronize.", default=None)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Don't ask for confirmation. Confirmation is needed when "
    "no snapshot name is provided.",
)
def session_sync(snapshot: Optional[str], name: Optional[str], yes: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    resp = send_json_request(
        "project_sessions", {"project_id": project_id, "session_name": name}
    )
    sessions = resp["sessions"]

    if len(sessions) == 0:
        raise click.ClickException(
            "No active session matching pattern {} found".format(name)
        )

    # Sync the snapshot to all matching sessions.
    for session in sessions:
        send_json_request(
            "session_sync",
            {"session_id": session["id"], "snapshot_uuid": snapshot},
            post=True,
        )


@session_cli.command(
    name="execute",
    context_settings=dict(ignore_unknown_options=True,),
    help="Execute a command in a session.",
)
@click.argument("command_name", required=False)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "--shell",
    help="If set, run the command as a raw shell command instead "
    "of looking up the command in the project.yaml.",
    is_flag=True,
)
@click.option("--name", help="Name of the session to run this command on", default=None)
def session_execute(
    command_name: Optional[str], args: List[str], shell: bool, name: Optional[str]
) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    resp = send_json_request(
        "project_sessions", {"project_id": project_id, "session_name": name}
    )
    sessions = resp["sessions"]

    if len(sessions) == 0:
        raise click.ClickException(
            "No active session matching pattern {} found".format(name)
        )

    # Get the actual command to run. This also validates the command,
    # which should be done before the command is executed.
    try:
        (command_to_run, parsed_args, config) = project_definition.get_command_info(
            command_name, args, shell, wildcards=False
        )
    except ValueError as e:
        raise click.ClickException(e)  # type: ignore
    if command_name and shell:
        command_name = " ".join([command_name] + list(args))
    for session in sessions:
        resp = send_json_request(
            "session_execute",
            {
                "session_id": session["id"],
                "name": command_name,
                "params": parsed_args,
                "shell": shell,
            },
            post=True,
        )


@session_cli.command(name="logs", help="Show logs for the current session.")
@click.option("--name", help="Name of the session to run this command on", default=None)
@click.option("--command-id", help="ID of the command to get logs for", default=None)
def session_logs(name: Optional[str], command_id: Optional[int]) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    # If the command_id is not specified, determine it by getting the
    # last run command from the active session.
    if not command_id:
        resp = send_json_request(
            "project_sessions", {"project_id": project_id, "session_name": name}
        )
        sessions = resp["sessions"]
        if len(sessions) == 0:
            raise click.ClickException(
                "No active session matching pattern {} found".format(name)
            )
        if len(sessions) > 1:
            raise click.ClickException(
                "Multiple active sessions matching pattern {} found".format(name)
            )
        session = sessions[0]
        resp = send_json_request("session_describe", {"session_id": session["id"]})
        # Search for latest run command
        last_created_at = datetime.datetime.min
        for command in resp["commands"]:
            created_at = deserialize_datetime(command["created_at"])
            if created_at > last_created_at:
                last_created_at = created_at
                command_id = command["session_command_id"]
        if not command_id:
            raise click.ClickException(
                "No comand was run yet on the latest active session {}".format(
                    session["name"]
                )
            )
    resp_out = send_json_request(
        "session_execution_logs",
        {
            "session_command_id": command_id,
            "log_type": "out",
            "start_line": 0,
            "end_line": 1000000000,
        },
    )
    resp_err = send_json_request(
        "session_execution_logs",
        {
            "session_command_id": command_id,
            "log_type": "err",
            "start_line": 0,
            "end_line": 1000000000,
        },
    )
    # TODO(pcm): We should have more options here in the future
    # (e.g. show only stdout or stderr, show only the tail, etc).
    print("stdout:")
    print(resp_out["lines"])
    print("stderr:")
    print(resp_err["lines"])


@session_cli.command(
    name="upload_command_logs", help="Upload logs for a command.", hidden=True
)
@click.option(
    "--command-id", help="ID of the command to upload logs for", type=int, default=None
)
def session_upload_command_logs(command_id: Optional[int]) -> None:
    resp = send_json_request(
        "session_upload_command_logs", {"session_command_id": command_id}, post=True
    )
    assert resp["session_command_id"] == command_id

    for source, target in resp["locations"].items():
        copy_file(True, source, target, download=False)


@session_cli.command(
    name="finish_command", help="Finish executing a command.", hidden=True
)
@click.option(
    "--command-id", help="ID of the command to finish", type=int, required=True
)
def session_finish_command(command_id: int) -> None:
    with open(execution_log_name(command_id) + ".status") as f:
        status_code = int(f.read().strip())
    resp = send_json_request(
        "session_finish_command",
        {"session_command_id": command_id, "status_code": status_code},
        post=True,
    )
    assert resp["session_command_id"] == command_id


@session_cli.command(
    name="setup_autosync",
    help="Set up automatic synchronization on the server side.",
    hidden=True,
)
@click.argument("session_id", type=int, required=True)
def session_setup_autosync(session_id: int) -> None:
    project_definition = load_project_or_throw()

    autosync_runner = AutosyncRunner()
    # Set autosync folder to the project directory.
    autosync_runner.add_or_update_project_folder(
        project_definition.config["name"],
        os.path.expanduser("~/" + project_definition.config["name"]),
    )
    device_id = autosync_runner.get_device_id()

    send_json_request(
        "session_autosync_started",
        {"session_id": session_id, "device_id": device_id},
        post=True,
    )

    autosync_runner.start_autosync(True)


@session_cli.command(
    name="autosync_add_device",
    help="Add device to autosync config on the server side.",
    hidden=True,
)
@click.argument("device_id", type=str, required=True)
def session_autosync_add_device(device_id: str) -> None:
    project_definition = load_project_or_throw()

    autosync_runner = AutosyncRunner()
    autosync_runner.add_device(project_definition.config["name"], device_id)
    # Restart syncthing.
    autosync_runner.kill_autosync()
    autosync_runner.start_autosync(True)


@session_cli.command(
    name="autosync", help="Run the autosync daemon on the client side."
)
@click.option(
    "--name", help="The name of the session to setup autosync for.", default=None
)
@click.option("--verbose", help="Show output from autosync.", is_flag=True)
def session_autosync(name: Optional[str], verbose: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    print("Active project: " + project_definition.config["name"])
    print()

    resp = send_json_request(
        "session_list",
        {"project_id": project_id, "session_name": name, "active_only": True},
    )
    sessions = resp["sessions"]

    if len(sessions) == 0:
        raise click.ClickException("No active session found")

    if len(sessions) > 1:
        raise click.ClickException("Session matching {} not unique".format(name))

    session = sessions[0]

    print("Autosyncing with session {}".format(session["name"]))

    autosync_runner = AutosyncRunner()
    device_id = autosync_runner.get_device_id()

    while True:
        try:
            resp = send_json_request(
                "session_autosync_add_device",
                {"session_id": session["id"], "device_id": device_id},
                post=True,
            )
        except click.ClickException:
            print("Session {} still starting up, waiting...".format(session["name"]))
            time.sleep(5.0)
        else:
            break

    # Add the project folder.
    autosync_runner.add_or_update_project_folder(
        project_definition.config["name"], project_definition.root
    )

    # Add the remote device.
    autosync_runner.add_device(
        project_definition.config["name"], resp["remote_device_id"]
    )

    autosync_runner.start_autosync(verbose)


@session_cli.command(name="auth_start", help="Start the auth proxy", hidden=True)
def auth_start() -> None:
    from aiohttp import web

    web.run_app(auth_proxy_app)


@session_cli.command(name="stop", help="Stop the current session.")
@click.option("--name", help="Name of the session to stop", default=None)
@click.option(
    "--terminate", help="Terminate the session instead of stopping it.", is_flag=True
)
@click.pass_context
def session_stop(ctx: Any, name: Optional[str], terminate: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    resp = send_json_request(
        "project_sessions", {"project_id": project_id, "session_name": name}
    )
    sessions = resp["sessions"]
    if len(sessions) == 0:
        raise click.ClickException(
            "No active session matching pattern {} found".format(name)
        )

    for session in sessions:
        # Stop the session and mark it as stopped in the database.
        send_json_request(
            "session_stop",
            {"session_id": session["id"], "terminate": terminate},
            post=True,
        )


@session_cli.command(name="list", help="List all sessions of the current project.")
@click.option(
    "--name",
    help="Name of the session. If provided, this prints the snapshots that "
    "were applied and commands that ran for all sessions that match "
    "this name.",
    default=None,
)
@click.option("--all", help="List all sessions, including inactive ones.", is_flag=True)
def session_list(name: Optional[str], all: bool) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    print("Active project: " + project_definition.config["name"])

    resp = send_json_request(
        "session_list",
        {"project_id": project_id, "session_name": name, "active_only": not all},
    )
    sessions = resp["sessions"]

    if name is None:
        print()
        table = []
        for session in sessions:
            created_at = humanize_timestamp(deserialize_datetime(session["created_at"]))
            record = [session["name"], created_at, session["latest_snapshot_uuid"]]
            if all:
                table.append([" Y" if session["active"] else " N"] + record)
            else:
                table.append(record)
        if not all:
            print(
                tabulate.tabulate(
                    table, headers=["SESSION", "CREATED", "SNAPSHOT"], tablefmt="plain"
                )
            )
        else:
            print(
                tabulate.tabulate(
                    table,
                    headers=["ACTIVE", "SESSION", "CREATED", "SNAPSHOT"],
                    tablefmt="plain",
                )
            )
    else:
        sessions = [session for session in sessions if session["name"] == name]
        for session in sessions:
            resp = send_json_request("session_describe", {"session_id": session["id"]})

            print()
            snapshot_table = []
            for applied_snapshot in resp["applied_snapshots"]:
                snapshot_uuid = applied_snapshot["snapshot_uuid"]
                created_at = humanize_timestamp(
                    deserialize_datetime(applied_snapshot["created_at"])
                )
                snapshot_table.append([snapshot_uuid, created_at])
            print(
                tabulate.tabulate(
                    snapshot_table,
                    headers=[
                        "SNAPSHOT applied to {}".format(session["name"]),
                        "APPLIED",
                    ],
                    tablefmt="plain",
                )
            )

            print()
            command_table = []
            for command in resp["commands"]:
                created_at = humanize_timestamp(
                    deserialize_datetime(command["created_at"])
                )
                command_table.append(
                    [
                        " ".join(
                            [command["name"]]
                            + [
                                "{}={}".format(key, val)
                                for key, val in command["params"].items()
                            ]
                        ),
                        command["session_command_id"],
                        created_at,
                    ]
                )
            print(
                tabulate.tabulate(
                    command_table,
                    headers=[
                        "COMMAND run in {}".format(session["name"]),
                        "ID",
                        "CREATED",
                    ],
                    tablefmt="plain",
                )
            )


cli.add_command(project_cli)
cli.add_command(session_cli)
cli.add_command(snapshot_cli)
cli.add_command(aws_cli)
cli.add_command(version_cli)


def main() -> Any:
    return cli()


if __name__ == "__main__":
    main()
