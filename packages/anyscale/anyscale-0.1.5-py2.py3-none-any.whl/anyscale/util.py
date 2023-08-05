import boto3
import botocore
from botocore.config import Config
import click
import datetime
import json
import logging
import os
import requests
import yaml
from typing import Any, Dict, List, Tuple

import anyscale.conf
from anyscale.common import ENDPOINTS


logger = logging.getLogger(__file__)

BOTO_MAX_RETRIES = 5


def confirm(msg: str, yes: bool) -> Any:
    return None if yes else click.confirm(msg, abort=True)


def get_endpoint(endpoint: str) -> str:
    route = ENDPOINTS[endpoint]
    return "{}{}".format(anyscale.conf.ANYSCALE_HOST, route)


def load_credentials() -> str:
    # The environment variable ANYSCALE_CLI_TOKEN can be used to
    # overwrite the credentials in ~/.anyscale/credentials.json
    if "ANYSCALE_CLI_TOKEN" in os.environ:
        return os.environ["ANYSCALE_CLI_TOKEN"]
    path = os.path.expanduser("~/.anyscale/credentials.json")
    if not os.path.exists(path):
        raise click.ClickException(
            "Credentials not found. You need to create an account at {0} "
            "and then go to {0}/credentials and follow the instructions.".format(
                anyscale.conf.ANYSCALE_HOST
            )
        )
    with open(path) as f:
        try:
            credentials: Dict[str, str] = json.load(f)
        except json.JSONDecodeError as e:
            raise click.ClickException(e)  # type: ignore
    if "cli_token" not in credentials:
        raise click.ClickException("Credential file not valid, please regenerate it.")
    return credentials["cli_token"]


def send_json_request(
    endpoint: str, json_args: Dict[str, Any], post: bool = False
) -> Dict[str, Any]:
    if anyscale.conf.CLI_TOKEN is None:
        anyscale.conf.CLI_TOKEN = load_credentials()

    url = get_endpoint(endpoint)
    cookies = {"cli_token": anyscale.conf.CLI_TOKEN}
    try:
        if post:
            resp = requests.post(url, json=json_args, cookies=cookies)
        else:
            resp = requests.get(url, params=json_args, cookies=cookies)
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            "Failed to connect to anyscale server at {}".format(url)
        )

    if not resp.ok:
        raise click.ClickException("{}: {}.".format(resp.status_code, resp.text))
    json_resp: Dict[str, Any] = resp.json()
    if "error" in json_resp:
        raise click.ClickException("{}".format(json_resp["error"]))

    return json_resp


def serialize_datetime(d: datetime.datetime) -> str:
    # Make sure that overwriting the tzinfo in the line below is fine.
    # Note that we have to properly convert the timezone if one is
    # already specified. This can be done with the .astimezone method.
    assert d.tzinfo is None
    return d.replace(tzinfo=datetime.timezone.utc).isoformat()


def deserialize_datetime(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f+00:00")


def humanize_timestamp(timestamp: datetime.datetime) -> str:
    delta = datetime.datetime.utcnow() - timestamp
    offset = float(delta.seconds + (delta.days * 60 * 60 * 24))
    delta_s = int(offset % 60)
    offset /= 60
    delta_m = int(offset % 60)
    offset /= 60
    delta_h = int(offset % 24)
    offset /= 24
    delta_d = int(offset)

    if delta_d >= 1:
        return "{} day{} ago".format(delta_d, "s" if delta_d > 1 else "")
    if delta_h > 0:
        return "{} hour{} ago".format(delta_h, "s" if delta_h > 1 else "")
    if delta_m > 0:
        return "{} minute{} ago".format(delta_m, "s" if delta_m > 1 else "")
    else:
        return "{} second{} ago".format(delta_s, "s" if delta_s > 1 else "")


def execution_log_name(session_command_id: int) -> str:
    return "/tmp/ray_command_output_{session_command_id}".format(
        session_command_id=session_command_id
    )


def startup_log_name(session_id: int) -> str:
    return "/tmp/session_startup_logs_{session_id}".format(session_id=session_id)


def get_cluster_config(config_path: str) -> Any:
    with open(config_path) as f:
        cluster_config = yaml.safe_load(f)

    return cluster_config


def _resource(name: str, region: str) -> Any:
    boto_config = Config(retries={"max_attempts": BOTO_MAX_RETRIES})
    boto_session = boto3.session.Session()
    return boto_session.resource(name, region, config=boto_config)


def _client(name: str, region: str) -> Any:
    boto_config = Config(retries={"max_attempts": BOTO_MAX_RETRIES})
    boto_session = boto3.session.Session()
    return boto_session.client(name, region, config=boto_config)


def _get_role(role_name: str, region: str) -> Any:
    iam = _resource("iam", region)
    role = iam.Role(role_name)
    try:
        role.load()
        return role
    except botocore.exceptions.ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "NoSuchEntity":
            return None
        else:
            raise exc


def _get_user(user_name: str, region: str) -> Any:
    iam = _resource("iam", region)
    user = iam.User(user_name)
    try:
        user.load()
        return user
    except botocore.exceptions.ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "NoSuchEntity":
            return None
        else:
            raise exc


def get_available_regions() -> List[str]:
    boto_session = boto3.session.Session()
    client = boto_session.client("ec2")
    return [region["RegionName"] for region in client.describe_regions()["Regions"]]
