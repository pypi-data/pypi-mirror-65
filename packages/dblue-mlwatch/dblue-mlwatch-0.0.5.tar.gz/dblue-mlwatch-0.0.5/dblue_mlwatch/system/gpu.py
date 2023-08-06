import os
import platform

from distutils import spawn
from subprocess import PIPE, Popen

from dblue_mlwatch.logger import logger


def safe_float_cast(num_str):
    try:
        number = float(num_str)
    except ValueError:
        number = float('nan')
    return number


def get_gpu_usage():
    if platform.system() == "Windows":
        # If the platform is Windows and nvidia-smi 
        # could not be found from the environment path, 
        # try to find it from system drive with default installation path
        nvidia_smi = spawn.find_executable('nvidia-smi')
        if nvidia_smi is None:
            nvidia_smi = "%s\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe" % os.environ['systemdrive']
    else:
        nvidia_smi = "nvidia-smi"

    # Get ID, processing and memory utilization for all GPUs

    query_params = ",".join([
        'index',
        'uuid',
        'utilization.gpu',
        'memory.total',
        'memory.used',
        'memory.free',
        'driver_version',
        'name',
        'gpu_serial',
        'display_active',
        'display_mode',
        'temperature.gpu',
    ])

    try:
        p = Popen([
            nvidia_smi,
            "--query-gpu={}".format(query_params),
            "--format=csv,noheader,nounits"
        ], stdout=PIPE
        )
        stdout, _ = p.communicate()
    except Exception as e:
        logger.exception(e)
        return {}

    output = stdout.decode('UTF-8')

    lines = output.split(os.linesep)

    num_devices = len(lines) - 1
    gpus = {}

    for g in range(num_devices):
        line = lines[g]
        values = line.split(', ')

        info = {
            'device_id': int(values[0]),
            'uuid': values[1],
            'utilization': safe_float_cast(values[2]) / 100,
            'memory_total': safe_float_cast(values[3]),
            'memory_used': safe_float_cast(values[4]),
            'memory_free': safe_float_cast(values[5]),
            'driver': values[6],
            'name': values[7],
            'temp': safe_float_cast(values[11]),

        }

        gpus['device_id'] = info
    return gpus
