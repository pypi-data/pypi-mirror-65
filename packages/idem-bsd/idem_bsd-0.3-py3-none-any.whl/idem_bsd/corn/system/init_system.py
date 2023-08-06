import aiofiles
import logging
import os
import shutil

log = logging.getLogger(__name__)


async def load_init(hub):
    log.debug("Adding init grain")
    hub.corn.CORN.init = "init"

    system = "/run/systemd/system"
    cmdline = "/proc/1/cmdline"

    if shutil.which("rc"):
        # The first choice for most BSD systems
        hub.corn.CORN.init = "rc"
    elif os.path.exists(system) and os.stat(system):
        hub.corn.CORN.init = "systemd"
    elif os.path.exists(cmdline):
        async with aiofiles.open("/proc/1/cmdline") as fhr:
            init_cmdline = (await fhr.read()).replace("\x00", " ").split()
            if len(init_cmdline) >= 1:
                init_bin = shutil.which(init_cmdline[0])
                if init_bin.endswith("bin/init"):
                    supported_inits = (b"upstart", b"sysvinit", b"systemd")
                    edge_len = max(len(x) for x in supported_inits) - 1
                    buf_size = hub.OPT.get("file_buffer_size", 262144)
                    try:
                        async with aiofiles.open(init_bin, "rb") as fp_:
                            edge = b""
                            buf = (await fp_.read(buf_size)).lower()
                            while buf:
                                buf = edge + buf
                                for item in supported_inits:
                                    if item in buf:
                                        item = item.decode("utf-8")
                                        hub.corn.CORN.init = item
                                        buf = b""
                                        break
                                edge = buf[-edge_len:]
                                buf = (await fp_.read(buf_size)).lower()
                    except (IOError, OSError) as exc:
                        log.error(
                            "Unable to read from init_bin (%s): %s", init_bin, exc
                        )
                elif shutil.which("supervisord") in init_cmdline:
                    hub.corn.CORN.init = "supervisord"
                elif shutil.which("dumb-init") in init_cmdline:
                    # https://github.com/Yelp/dumb-init
                    hub.corn.CORN.init = "dumb-init"
                elif shutil.which("tini") in init_cmdline:
                    # https://github.com/krallin/tini
                    hub.corn.CORN.init = "tini"
                elif init_cmdline == ["runit"]:
                    hub.corn.CORN.init = "runit"
                elif "/sbin/my_init" in init_cmdline:
                    # Phusion Base docker container use runit for srv mgmt, but
                    # my_init as pid1
                    hub.corn.CORN.init = "runit"
                else:
                    log.debug(
                        "Could not determine init system from command line: (%s)",
                        " ".join(init_cmdline),
                    )
            else:
                # Emtpy init_cmdline
                log.warning("Unable to fetch data from /proc/1/cmdline")
