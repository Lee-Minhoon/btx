def roi(initial: float, current: float):
    return (current - initial) / initial * 100


def annual_roi(initial: float, current: float, days: int):
    return ((current / initial) ** (365 / days) - 1) * 100
