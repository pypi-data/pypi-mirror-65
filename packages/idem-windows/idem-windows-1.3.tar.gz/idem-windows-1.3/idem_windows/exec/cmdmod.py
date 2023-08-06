# -*- coding: utf-8 -*-
import asyncio
import logging
import os
import re
import shlex
import traceback
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
            cwd = os.path.abspath(os.sep)
    else:
        # Handle edge cases where numeric/other input is entered, and would be
        # yaml-ified into non-string types
        cwd = str(cwd)

    if not os.path.isabs(cwd) or not os.path.isdir(cwd):
        raise SystemError(
            f"Specified cwd '{cwd}' either not absolute or does not exist"
        )

    return cwd


async def _escape_argument(arg: str, escape: bool = True):
    """
    Escape the argument for the cmd.exe shell.
    See http://blogs.msdn.com/b/twistylittlepassagesallalike/archive/2011/04/23/everyone-quotes-arguments-the-wrong-way.aspx

    First we escape the quote chars to produce a argument suitable for
    CommandLineToArgvW. We don't need to do this for simple arguments.

    Args:
        arg (str): a single command line argument to escape for the cmd.exe shell

    Kwargs:
        escape (bool): True will call the escape_for_cmd_exe() function
                       which escapes the characters '()%!^"<>&|'. False
                       will not call the function and only quotes the cmd

    Returns:
        str: an escaped string suitable to be passed as a program argument to the cmd.exe shell
    """
    if not arg or re.search(r'(["\s])', arg):
        arg = '"' + arg.replace('"', r"\"") + '"'

    if not escape:
        return arg
    return await _escape_for_cmd_exe(arg)


async def _escape_for_cmd_exe(arg: str) -> str:
    """
    Escape an argument string to be suitable to be passed to
    cmd.exe on Windows

    This method takes an argument that is expected to already be properly
    escaped for the receiving program to be properly parsed. This argument
    will be further escaped to pass the interpolation performed by cmd.exe
    unchanged.

    Any meta-characters will be escaped, removing the ability to e.g. use
    redirects or variables.

    Args:
        arg (str): a single command line argument to escape for cmd.exe

    Returns:
        str: an escaped string suitable to be passed as a program argument to cmd.exe
    """
    meta_chars = '()%!^"<>&|'
    meta_re = re.compile(
        "(" + "|".join(re.escape(char) for char in list(meta_chars)) + ")"
    )
    meta_map = {char: "^{0}".format(char) for char in meta_chars}

    def escape_meta_chars(m):
        char = m.group(1)
        return meta_map[char]

    return meta_re.sub(escape_meta_chars, arg)


async def _sanitize_cmd(cmd: str or List[str]) -> str or List[str]:
    if not isinstance(cmd, list):
        cmd = cmd.split()
    # Return stripped command string copies to improve logging.
    # Use shlex.quote to properly escape whitespace and special characters in strings passed to shells
    if isinstance(cmd, list):
        cmd = [shlex.quote(str(x).strip()) for x in cmd]
    else:
        cmd = shlex.quote(cmd.strip())
    return cmd


async def _sanitize_kwargs(**kwargs):
    """
    Only pass through approved kwargs
    """
    new_kwargs = {}
    if "stdin_raw_newlines" in kwargs:
        new_kwargs["stdin_raw_newlines"] = kwargs["stdin_raw_newlines"]
    return new_kwargs


async def _powershell_mod(cmd: str or List[str]) -> str or List[str]:
    # If we were called by script(), then fakeout the Windows
    # shell to run a Powershell script.
    # Else just run a Powershell command.
    stack = traceback.extract_stack(limit=2)

    # extract_stack() returns a list of tuples.
    # The last item in the list [-1] is the current method.
    # The third item[2] in each tuple is the name of that method.
    if stack[-2][2] == "script":
        return (
            f"Powershell -NonInteractive -NoProfile -ExecutionPolicy Bypass -File {cmd}"
        )
    else:
        return 'Powershell -NonInteractive -NoProfile "{0}"'.format(
            cmd.replace('"', '\\"')
        )


async def run(
    hub,
    cmd: str or List[str],
    cwd: str = None,
    shell: bool = False,
    stdin: str = None,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    env: Dict[str, Any] = None,
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

    :param timeout: A timeout in seconds for the executed process to return.
    """
    cwd = await _sanitize_cwd(cwd)
    env = await _sanitize_env(env)
    cmd = await _sanitize_cmd(cmd)

    # TODO this corn doesn't exist yet
    if hub.corn.CORN.get("shell", "") == "powershell.exe":
        log.debug("Escaping command for powershell.exe")
        cmd = await _powershell_mod(cmd)
    elif hub.corn.CORN.get("shell", "") == "cmd.exe":
        log.debug("Escaping command for cmd.exe")
        cmd = await _escape_argument(cmd)

    new_kwargs = {
        "cwd": cwd,
        "env": env if env else os.environ.copy(),
        "stdout": stdout,
        "stderr": stderr,
        "shell": shell,
        **await _sanitize_kwargs(**kwargs),
    }

    ret = {}
    log.debug(f"Executing command: {' '.join(cmd)}")
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


async def powershell(hub, cmd):
    # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    raise NotImplementedError
