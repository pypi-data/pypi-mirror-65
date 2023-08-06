import logging
import re
import shutil

log = logging.getLogger(__name__)


async def load_lspci(hub):
    gpus = []

    lspci = shutil.which("lspci")
    if not lspci:
        log.debug(
            "The `lspci` binary is not available on the system. GPU corn "
            "will not be available."
        )
        return

    # dominant gpu vendors to search for (MUST be lowercase for matching below)
    known_vendors = [
        "nvidia",
        "amd",
        "ati",
        "intel",
        "cirrus logic",
        "vmware",
        "matrox",
        "aspeed",
    ]
    gpu_classes = ("vga compatible controller", "3d controller")

    devs = []
    try:
        lspci_out = (await hub.exec.cmd.run(f"{lspci} -vmm"))["stdout"]

        cur_dev = {}
        error = False
        # Add a blank element to the lspci_out.splitlines() list,
        # otherwise the last device is not evaluated as a cur_dev and ignored.
        lspci_list = lspci_out.splitlines()
        lspci_list.append("")
        for line in lspci_list:
            # check for record-separating empty lines
            if line == "":
                if cur_dev.get("Class", "").lower() in gpu_classes:
                    devs.append(cur_dev)
                cur_dev = {}
                continue
            if re.match(r"^\w+:\s+.*", line):
                key, val = line.split(":", 1)
                cur_dev[key.strip()] = val.strip()
            else:
                error = True
                log.debug("Unexpected lspci output: '%s'", line)

        if error:
            log.warning(
                "Error loading corn, unexpected linux_gpu_data output, "
                "check that you have a valid shell configured and "
                "permissions to run lspci command"
            )
    except OSError:
        pass

    for gpu in devs:
        vendor_strings = gpu["Vendor"].lower().split()
        # default vendor to 'unknown', overwrite if we match a known one
        vendor = "unknown"
        for name in known_vendors:
            # search for an 'expected' vendor name in the list of strings
            if name in vendor_strings:
                vendor = name
                break
        gpus.append({"model": gpu["Device"], "vendor": vendor})

    hub.corn.CORN.gpus = gpus
    hub.corn.CORN.num_gpus = len(gpus)
