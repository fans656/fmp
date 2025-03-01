import bisect


def find_nearest(items: list[dict], value: float, key: str):
    index = bisect.bisect(items, value, key=lambda d: d[key])
    if index == len(items):
        return items[-1]
    elif index == 0:
        return items[index]
    else:
        lhs = items[index - 1]
        rhs = items[index]
        if abs(value - items[index - 1][key]) <= abs(items[index][key] - value):
            return items[index - 1]
        else:
            return items[index]
