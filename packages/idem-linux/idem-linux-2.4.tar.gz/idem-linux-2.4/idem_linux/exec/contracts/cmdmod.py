# -*- coding: utf-8 -*-
from typing import Any, Dict, List


async def sig_run(
    hub,
    cmd: str or List[str],
    cwd: str,
    stdin: str,
    stdout: int,
    stderr: int,
    shell: bool,
    env: Dict[str, Any],
    umask: str,
    timeout: int or float,
    **kwargs,
) -> Dict[str, Any]:
    pass
