def get_size(bytes_, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    value = ''
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes_ < factor:
            value = f"{bytes_:.2f}{unit}{suffix}"
            break
        bytes_ /= factor

    return value
