async def load_computer_name(hub):
    hub.corn.CORN.computer_name = (await hub.exec.cmd.run("hostname"))["stdout"].strip()
