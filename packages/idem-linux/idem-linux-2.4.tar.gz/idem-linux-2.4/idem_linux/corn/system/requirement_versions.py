import logging
import os
import pathlib
import re
import subprocess
import sys

log = logging.getLogger(__name__)


async def load_python_version(hub):
    hub.corn.CORN.pythonversion = list(sys.version_info)


async def load_pip_versions(hub):
    """
    Get the versions of required pip packages
    """
    root_dir = pathlib.Path(
        os.path.join(os.path.dirname(__file__))
    ).parent.parent.parent
    requirements_test = os.path.join(root_dir, "requirements-test.txt")
    requirements = os.path.join(root_dir, "requirements.txt")
    reqs = {}
    for req_file in (requirements, requirements_test):
        if not os.path.isfile(req_file):
            continue
        with open(req_file, "r") as _fh:
            for line in _fh:
                split = re.split("[ <>=]", line.strip())
                name = split[0].lower()
                version = split[-1].lower()
                if name == version:
                    version = None
                reqs[name] = version
    try:
        modules = {}
        proc = subprocess.Popen(
            [sys.executable, "-m", "pip", "freeze"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = proc.communicate()
        if proc.wait():
            raise OSError(f"Error running command: {stderr.decode().strip()}")
        for x in stdout.decode().split():
            if "==" in x:
                name, version = x.split("==")
            elif "#egg=" in x:
                version, name = x.split("#egg=")
            else:
                name = x
                version = None

            # pip is agnostic about case so we will prefer lower
            name = name.lower()
            if name in reqs:
                modules[name] = version

        hub.corn.CORN.requirement_versions = modules
    except OSError as e:
        log.error(f"Error running pip command: {e}")
        hub.corn.CORN.requirement_versions = reqs
