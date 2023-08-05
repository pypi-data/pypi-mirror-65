# -*- coding: utf-8 -*-
import asyncio
import functools
import logging
import os
import shlex
from typing import Any, Dict, List

log = logging.getLogger(__name__)

__virtualname__ = "cmd"


async def _sanitize_env(env: Dict[str, Any]) -> Dict[str, str] or None:
    if env is None:
        return
    for bad_env_key in (k for k, v in env.items() if v is None):
        log.error(
            "Environment variable '%s' passed without a value. "
            "Setting value to an empty string",
            bad_env_key,
        )
        env[bad_env_key] = ""
    return env


async def _sanitize_cwd(cwd: str or None) -> str:
    # salt-minion is running as. Defaults to home directory of user under which
    # the minion is running.
    if not cwd:
        cwd = os.path.expanduser("~")

        # make sure we can access the cwd
        # when run from sudo or another environment where the euid is
        # changed ~ will expand to the home of the original uid and
        # the euid might not have access to it. See issue #1844
        if not os.access(cwd, os.R_OK):
            cwd = "/"
    else:
        # Handle edge cases where numeric/other input is entered, and would be
        # yaml-ified into non-string types
        cwd = str(cwd)

    if not os.path.isabs(cwd) or not os.path.isdir(cwd):
        raise SystemError(
            f"Specified cwd '{cwd}' either not absolute or does not exist"
        )

    return cwd


async def _sanitize_cmd(cmd: str or List[str]) -> str or List[str]:
    if not isinstance(cmd, list):
        cmd = cmd.split()
    # Return stripped command string copies to improve logging.
    # Use shlex.quote to properly escape whitespace and special characters in strings passed to shells
    if isinstance(cmd, list):
        cmd = [shlex.quote(str(x).strip()) for x in cmd]
    else:
        cmd = shlex.quote(cmd)
    return cmd


async def _sanitize_umask(umask: str) -> int or None:
    if umask is None:
        return

    _umask = str(umask).lstrip("0")

    if _umask == "":
        raise SystemError("Zero umask is not allowed.")

    try:
        return int(_umask, 8)
    except ValueError:
        raise SystemError("Invalid umask: '{0}'".format(umask))


async def _sanitize_kwargs(**kwargs):
    """
    Only pass through approved kwargs
    """
    new_kwargs = {}
    if "stdin_raw_newlines" in kwargs:
        new_kwargs["stdin_raw_newlines"] = kwargs["stdin_raw_newlines"]
    return new_kwargs


async def run(
    hub,
    cmd: str or List[str],
    cwd: str = None,
    shell: bool = False,
    stdin: str = None,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    env: Dict[str, Any] = None,
    umask: str = None,
    timeout: int or float = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Execute the passed command and return the output as a string

    :param cmd: The command to run. ex: ``ls -lart /home``

    :param cwd: The directory from which to execute the command. Defaults
        to the home directory of the user specified by ``runas`` (or the user
        under which Salt is running if ``runas`` is not specified).

    :param stdin: A string of standard input can be specified for the
        command to be run using the ``stdin`` parameter. This can be useful in
        cases where sensitive information must be read from standard input.

    :param shell: If ``False``, let python handle the positional
        arguments. Set to ``True`` to use shell features, such as pipes or
        redirection.

    :param stdout:

    :param stderr:

    :param env: Environment variables to be set prior to execution.

        .. note::
            When passing environment variables on the CLI, they should be
            passed as the string representation of a dictionary.

            .. code-block:: bash

                salt myminion cmd.run 'some command' env='{"FOO": "bar"}'
    :param umask: The umask (in octal) to use when running the command.

    :param timeout: A timeout in seconds for the executed process to return.
    """
    cmd = await _sanitize_cmd(cmd)
    cwd = await _sanitize_cwd(cwd)
    env = await _sanitize_env(env)
    umask = await _sanitize_umask(umask)

    new_kwargs = {
        "cwd": cwd,
        "env": env if env else os.environ.copy(),
        "preexec_fn": functools.partial(os.umask, umask) if umask else None,
        "stdout": stdout,
        "stderr": stderr,
        "shell": shell,
        **await _sanitize_kwargs(**kwargs),
    }

    ret = {}
    # Run the command
    if shell:
        proc = await asyncio.create_subprocess_shell(" ".join(cmd), **new_kwargs)
    else:
        proc = await asyncio.create_subprocess_exec(*cmd, **new_kwargs)

    # This is where the magic happens
    out, err = await asyncio.wait_for(proc.communicate(input=stdin), timeout=timeout)

    ret["pid"] = proc.pid
    ret["retcode"] = await asyncio.wait_for(proc.wait(), timeout=timeout)
    ret["stdout"] = out.decode() if out is not None else ""
    ret["stderr"] = err.decode() if err is not None else ""

    return ret
