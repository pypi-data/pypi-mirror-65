import logging
import re
import shutil
from typing import Dict, List

log = logging.getLogger(__name__)

KNOWN_VENDORS = [
    "nvidia",
    "amd",
    "ati",
    "intel",
    "cirrus logic",
    "vmware",
    "matrox",
    "aspeed",
]


async def _load_pcictl(hub) -> List[Dict[str, str]]:
    """
    num_gpus: int
    gpus:
      - vendor: nvidia|amd|ati|...
        model: string
    """
    gpus = []

    pcictl = shutil.which("pcictl")
    if pcictl:
        out = await hub.exec.cmd.run([pcictl, "pci0", "list"])
        for line in out.stdout.strip().splitlines():
            for vendor in KNOWN_VENDORS:
                vendor_match = re.match(
                    fr"[0-9:]+ ({vendor}) (.+) \(VGA .+\)", line, re.IGNORECASE
                )
                if vendor_match:
                    gpus.append(
                        {
                            "vendor": vendor_match.group(1),
                            "model": vendor_match.group(2),
                        }
                    )
    return gpus


async def _load_pciconf(hub) -> List[Dict[str, str]]:
    gpus = []
    pciconf = shutil.which("pciconf")
    if pciconf:
        ret = await hub.exec.cmd.run([pciconf, "-l", "-v"])
        if not ret.retcode:
            device = {"model": None, "vendor": "unknown"}
            for line in ret.stdout.splitlines():
                if " = " in line:
                    key, val = line.split("=", 1)
                    key = key.strip(" ")
                    val = val.strip("'\" ")
                    if key == "vendor":
                        device["vendor"] = val
                    elif key == "device":
                        device["model"] = val
                    elif key == "class" and val == "display":
                        gpus.append(device.copy())
    return gpus


async def _load_glxinfo(hub) -> List[Dict[str, str]]:
    """Mesa library for detecting gpu info"""
    gpus = []
    glxinfo = shutil.which("glxinfo")
    if glxinfo:
        ret = await hub.exec.cmd.run([glxinfo, "-B"])
        if not ret.retcode:
            for line in ret.stdout.splitlines():
                if "Device:" in line:
                    gpus.append(
                        {
                            "model": line.split(":")[1].split("(")[0].strip(),
                            "vendor": "unknown",
                        }
                    )
    return gpus


async def load_gpudata(hub):
    hub.corn.CORN.gpus = (
        await _load_pcictl(hub) or await _load_pciconf(hub) or await _load_glxinfo(hub)
    )
    hub.corn.CORN.num_gpus = len(hub.corn.CORN.gpus)
