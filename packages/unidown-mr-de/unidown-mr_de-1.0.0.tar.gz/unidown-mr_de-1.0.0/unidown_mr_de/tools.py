def sizeof_fmt(num, suffix: str = 'B'):
    """
    Converts a number of units into a human readable string.
    https://stackoverflow.com/a/1094933

    :param num: number in suffix units
    :param suffix: unit
    :return: human readable string
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f"{num:.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"
