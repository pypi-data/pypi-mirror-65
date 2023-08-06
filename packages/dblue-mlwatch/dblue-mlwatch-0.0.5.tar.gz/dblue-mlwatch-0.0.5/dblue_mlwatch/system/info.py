import platform
import re
import uuid

import psutil

from dblue_mlwatch.logger import logger
from dblue_mlwatch.utils import get_size


def get_os_info():
    try:
        info = {
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
        }
        return info
    except Exception:
        logger.exception("Failed to read operating system information")


def get_hardware_info():
    try:
        memory = psutil.virtual_memory()

        info = {
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'mac_address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'cores': psutil.cpu_count(),
            'memory': get_size(memory.total),
        }

        return info
    except Exception:
        logger.exception("Failed to read hardware information")
