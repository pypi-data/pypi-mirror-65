import shutil

import psutil


def get_disk_partition_usage():
    # get all disk partitions
    disk_partitions = psutil.disk_partitions()
    partitions = {}

    for partition in disk_partitions:
        info = {
            'name': partition.device,
            'mount_point': partition.mountpoint,
            'fs_type': partition.fstype,
        }

        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can happen when disk is not ready
            partitions[partition.device] = info
            continue

        info['size'] = partition_usage.total
        info['used'] = partition_usage.used
        info['free'] = partition_usage.free
        info['used_percent'] = partition_usage.percent

        partitions[partition.device] = info

    return partitions


def get_disk_usage():
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    total, used, free = shutil.disk_usage("/")

    usage = {
        'total': total,
        'used': used,
        'free': free,
        'read_count': disk_io.read_count,
        'write_count': disk_io.write_count,
        'read_bytes': disk_io.read_bytes,
        'write_bytes': disk_io.write_bytes,
    }

    return usage
