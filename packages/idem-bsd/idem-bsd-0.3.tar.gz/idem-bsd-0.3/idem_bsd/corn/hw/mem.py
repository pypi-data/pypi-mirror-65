import shutil


async def _load_swapctl(hub) -> str:
    swapctl = shutil.which("swapctl")

    swap_data = (await hub.exec.cmd.run([swapctl, "-sk"])).stdout.strip()
    if swap_data == "no swap devices configured":
        return ""
    else:
        return swap_data.split(" ")[1]


async def _load_sysctl_swap(hub) -> str:
    sysctl = shutil.which("sysctl")
    if sysctl:
        return (await hub.exec.cmd.run([sysctl, "-n", "vm.swap_total"])).stdout


async def load_swap(hub):
    """
    Return the swap information for BSD-like systems
    """
    hub.corn.CORN.swap_total = (
        int(await _load_swapctl(hub) or await _load_sysctl_swap(hub) or 0)
        // 1024
        // 1024
    )


async def load_meminfo(hub):
    """
    Return the memory information for BSD-like systems
    """
    hub.corn.CORN.mem_total = 0

    sysctl = shutil.which("sysctl")

    if sysctl:
        mem = int((await hub.exec.cmd.run([sysctl, "-n", "hw.physmem"])).stdout)
        if mem <= 0:
            mem = int((await hub.exec.cmd.run([sysctl, "-n", "hw.physmem64"])).stdout)
        hub.corn.CORN.mem_total = mem // 1024 // 1024
