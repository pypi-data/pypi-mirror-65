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
        hub.corn.CORN.osarch,
    ) = os.uname()

    assert hub.corn.CORN.kernel.endswith(
        "BSD"
    ), "idem-bsd is only intended for BSD systems"

    # Hard coded grains for BSD
    hub.corn.CORN.os_family = "BSD"
    hub.corn.CORN.ps = "ps auxwww"
