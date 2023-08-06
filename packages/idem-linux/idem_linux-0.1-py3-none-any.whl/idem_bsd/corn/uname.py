import os


async def load_uname(hub):
    """
    Verify that POP linux is running on BSD
    """
    (
        hub.corn.CORN.kernel,
        hub.corn.CORN.nodename,
        hub.corn.CORN.kernelrelease,
        hub.corn.CORN.kernelversion,
        hub.corn.CORN.cpuarch,
    ) = os.uname()

    assert (
        hub.corn.CORN.kernel == "FreeBSD"
    ), "idem-bsd is only intended for BSD systems"

    hub.corn.CORN.ps = "ps -efHww"
