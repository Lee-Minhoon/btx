def roi(initial: float, current: float):
    if initial == 0:
        return 0
    return (current - initial) / initial * 100


def annual_roi(initial: float, current: float, days: int):
    return ((current / initial) ** (365 / days) - 1) * 100


def annual_roi_from_roi(roi: float, days: int):
    return ((1 + roi / 100) ** (365 / days) - 1) * 100
