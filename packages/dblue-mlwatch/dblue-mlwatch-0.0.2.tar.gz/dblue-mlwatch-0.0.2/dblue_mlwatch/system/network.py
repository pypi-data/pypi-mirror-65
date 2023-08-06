import psutil


def get_network_usage():
    # get IO statistics since boot
    net_io = psutil.net_io_counters()

    usage = {
        'bytes_sent': net_io.bytes_sent,
        'bytes_received': net_io.bytes_recv,
        'packets_sent': net_io.packets_sent,
        'packets_received': net_io.packets_recv,
        'error_in': net_io.errin,
        'error_out': net_io.errout,
        'drop_in': net_io.dropin,
        'drop_out': net_io.dropout,
    }

    return usage
