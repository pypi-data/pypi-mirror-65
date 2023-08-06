import psutil

from dblue_mlwatch.logger import logger


def get_cpu_load(interval=1):
    try:
        cpu_loads = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]

        if interval == 1:
            return cpu_loads[0]

        if interval == 5:
            return cpu_loads[1]

        if interval == 15:
            return cpu_loads[2]

        return 0
    except Exception as e:
        logger.exception(e)
        return 0


def get_cpu_usage():
    return {
        'load': get_cpu_load(),
        'usage_percent': psutil.cpu_percent(),
    }
