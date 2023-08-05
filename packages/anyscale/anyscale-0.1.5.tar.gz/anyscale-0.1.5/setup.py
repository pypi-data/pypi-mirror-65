from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# mypy: ignore-errors

import os
import re
import shutil

from setuptools import setup, find_packages, Distribution
import setuptools.command.build_ext as _build_ext


def find_version(path):
    with open(path) as f:
        match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE)
        if match:
            return match.group(1)
        raise RuntimeError("Unable to find version string.")


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = True


except ImportError:
    bdist_wheel = None


class build_ext(_build_ext.build_ext):
    def run(self):
        import io
        import requests
        import tarfile
        import tempfile
        import bz2

        work_dir = tempfile.mkdtemp()
        try:
            for system in ["linux", "macos"]:
                version = "v1.3.4"
                filename = "syncthing-{}-amd64-{}".format(system, version)
                url = (
                    "https://github.com/syncthing/syncthing/"
                    "releases/download/{}/{}.tar.gz".format(version, filename)
                )
                content = requests.get(url).content
                syncthing = tarfile.open(None, "r", io.BytesIO(content))
                try:
                    syncthing.extractall(work_dir)
                finally:
                    syncthing.close()
                # Copy the syncthing executable into the wheel.
                source = os.path.join(work_dir, filename, "syncthing")
                destination = os.path.join("anyscale", "syncthing-" + system)
                # Remove the file if it already exists to make sure old
                # versions get removed.
                try:
                    os.remove(destination)
                except OSError:
                    pass
                shutil.copy(source, destination)
                self.move_file(destination)

            for system in ["linux", "darwin"]:
                version = "0.9.6"
                filename = "restic_{}".format(version)
                url = (
                    "https://github.com/restic/restic/releases/download/"
                    "v{}/{}_{}_amd64.bz2".format(version, filename, system)
                )
                content = requests.get(url).content

                restic = bz2.decompress(content)
                with open(os.path.join(work_dir, filename), "wb") as f:
                    f.write(restic)

                # Copy the restic executable into the wheel.
                source = os.path.join(work_dir, filename)
                destination = os.path.join("anyscale", "restic-" + system)

                # Remove the file if it already exists to make sure old
                # versions get removed.
                try:
                    os.remove(destination)
                except OSError:
                    pass
                shutil.copy2(source, destination)
                os.chmod(destination, 0o755)
                self.move_file(destination)

        finally:
            shutil.rmtree(work_dir)

    def move_file(self, filename):
        # TODO(rkn): This feels very brittle. It may not handle all cases. See
        # https://github.com/apache/arrow/blob/master/python/setup.py for an
        # example.
        source = filename
        destination = os.path.join(self.build_lib, filename)
        # Create the target directory if it doesn't already exist.
        parent_directory = os.path.dirname(destination)
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)
        if not os.path.exists(destination):
            print("Copying {} to {}.".format(source, destination))
            shutil.copy(source, destination, follow_symlinks=True)


class BinaryDistribution(Distribution):
    def is_pure(self):
        return True

    def has_ext_modules(self):
        return True


setup(
    name="anyscale",
    version=find_version("anyscale/__init__.py"),
    author="Anyscale Inc.",
    description=("Command Line Interface for Anyscale"),
    packages=find_packages(),
    cmdclass={"bdist_wheel": bdist_wheel, "build_ext": build_ext},
    distclass=BinaryDistribution,
    setup_requires=["setuptools_scm"],
    install_requires=[
        "boto3",
        "Click>=7.0",
        "GitPython",
        "jsonschema",
        "ray",
        "requests",
        "tabulate",
        "aiohttp",
    ],
    entry_points={"console_scripts": ["anyscale=anyscale.scripts:main"]},
    include_package_data=True,
    zip_safe=False,
)
