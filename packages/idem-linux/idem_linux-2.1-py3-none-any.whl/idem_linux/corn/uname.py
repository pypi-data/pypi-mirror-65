import os


async def load_uname(hub):
    """
    Verify that POP linux is running on linux
    """
    (
        hub.corn.CORN.kernel,
        hub.corn.CORN.nodename,
        hub.corn.CORN.kernelrelease,
        hub.corn.CORN.kernelversion,
        hub.corn.CORN.cpuarch,
    ) = os.uname()

    assert (
        hub.corn.CORN.kernel == "Linux"
    ), "POP-Linux is only intended for Linux systems"

    if not hub.corn.CORN.get("ps"):
        hub.corn.CORN.ps = "ps -efHww"
