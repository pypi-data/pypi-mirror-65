import psutil


def get_memory_usage():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        'total': memory.total,
        'available': memory.available,
        'used': memory.used,
        'used_percent': memory.percent,
        'swap_total': swap.total,
        'swap_free': swap.free,
        'swap_used': swap.used,
        'swap_used_percent': swap.percent,
    }
