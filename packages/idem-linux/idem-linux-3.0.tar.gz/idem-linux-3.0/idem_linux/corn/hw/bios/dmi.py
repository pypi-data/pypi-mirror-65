"""
Get system specific hardware data from dmidecode

Provides
    biosversion
    productname
    manufacturer
    serialnumber
    biosreleasedate
    uuid

.. versionadded:: 0.9.5
"""
import aiofiles
import errno
import logging
import os
import shutil

log = logging.getLogger(__name__)

# TODO This file is a mess, refactor please


async def load_dmi(hub):
    name = "/sys/class/dmi/id"
    if os.path.exists(name):
        # On many Linux distributions basic firmware information is available via sysfs
        # requires CONFIG_DMIID to be enabled in the Linux kernel configuration
        sysfs_firmware_info = {
            "biosversion": "bios_version",
            "productname": "product_name",
            "manufacturer": "sys_vendor",
            "biosreleasedate": "bios_date",
            "uuid": "product_uuid",
            "serialnumber": "product_serial",
        }
        for key, fw_file in sysfs_firmware_info.items():
            contents_file = os.path.join("/sys/class/dmi/id", fw_file)
            if os.path.exists(contents_file):
                try:
                    async with aiofiles.open(contents_file, "r") as ifile:
                        hub.corn.CORN[key] = (await ifile.read()).strip()
                        if key == "uuid":
                            hub.corn.CORN.uuid = hub.corn.CORN.uuid.lower()
                except (IOError, OSError) as err:
                    # PermissionError is new to Python 3, but corresponds to the EACESS and
                    # EPERM error numbers. Use those instead here for PY2 compatibility.
                    if err.errno == errno.EACCES or err.errno == errno.EPERM:
                        # Skip the grain if non-root user has no access to the file.
                        pass


async def load_smbios(hub):
    if shutil.which("smbios"):
        if not hub.corn.CORN.get("biosversion"):
            hub.corn.CORN.biosversion = hub.exec.smbios.get("bios-version")
        if not hub.corn.CORN.get("productname"):
            hub.corn.CORN.productname = hub.exec.smbios.get("system-product-name")
        if not hub.corn.CORN.get("manufacturer"):
            hub.corn.CORN.manufacturer = hub.exec.smbios.get("system-manufacturer")
        if not hub.corn.CORN.get("biosreleasedate"):
            hub.corn.CORN.biosreleasedate = hub.exec.smbios.get("bios-release-date")
        if not hub.corn.CORN.get("uuid"):
            hub.corn.CORN.uuid = hub.exec.smbios.get("system-uuid").lower()
        for serial in (
            "system-serial-number",
            "chassis-serial-number",
            "baseboard-serial-number",
        ):
            serial = hub.exec.smbios.get(serial)
            if serial is not None:
                hub.corn.CORN.serialnumber = serial
                break


async def load_arm_linux(hub):
    if shutil.which("fw_printenv"):
        # ARM Linux devices expose UBOOT env variables via fw_printenv
        hwdata = {
            "manufacturer": "manufacturer",
            "serialnumber": "serial#",
            "productname": "DeviceDesc",
        }
        for grain_name, cmd_key in hwdata.items():
            result = await hub.exec.cmd.run(f"fw_printenv {cmd_key}")
            if result.retcode == 0:
                uboot_keyval = result.stdout.split("=")[1]
                hub.corn.CORN[grain_name] = await hub.corn.init.clean_value(
                    grain_name, uboot_keyval
                )
