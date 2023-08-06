async def load_cpe_name(hub):
    """
    Parse CPE_NAME data from the os-release

    Info: https://csrc.nist.gov/projects/security-content-automation-protocol/scap-specifications/cpe

    Note: cpe:2.3:part:vendor:product:version:update:edition:lang:sw_edition:target_sw:target_hw:other
          however some OS's do not have the full 13 elements, for example:
                CPE_NAME="cpe:2.3:o:amazon:amazon_linux:2"
    """
    # TODO where is cpe name set?
    if hub.corn.CORN.get("cpe_name"):
        cpe = hub.corn.CORN.get("cpe_name")
        if len(cpe) > 4 and cpe[0] == "cpe":
            if cpe[1].startswith("/"):  # WFN to URI
                (
                    hub.corn.CORN.vendor,
                    hub.corn.CORN.product,
                    hub.corn.CORN.version,
                ) = cpe[2:5]
                hub.corn.CORN.phase = cpe[5] if len(cpe) > 5 else None
                hub.corn.CORN.part = CPE_PARTS.get(cpe[1][1:])
            elif len(cpe) == 6 and cpe[1] == "2.3":  # WFN to a string
                (
                    hub.corn.CORN.vendor,
                    hub.corn.CORN.product,
                    hub.corn.CORN.version,
                ) = [x if x != "*" else None for x in cpe[3:6]]
                hub.corn.CORN.phase = None
                hub.corn.CORN.part = CPE_PARTS.get(cpe[2])
            elif 7 < len(cpe) <= 13 and cpe[1] == "2.3":  # WFN to a string
                (
                    hub.corn.CORN.vendor,
                    hub.corn.CORN.product,
                    hub.corn.CORN.version,
                    hub.corn.CORN.phase,
                ) = [x if x != "*" else None for x in cpe[3:7]]
                hub.corn.CORN.part = CPE_PARTS.get(cpe[2])
