def clamp(n, min_n, max_n):
    """
    Limits n to the bounds defined by minn and maxn.
    Source: https://stackoverflow.com/questions/5996881/how-to-limit-a-number-to-be-within-a-specified-range-python
    :param n: Number to be clamped
    :param min_n: Minimum value (inclusive)
    :param max_n: Maximum value (inclusive)
    :return:
    """
    if n < min_n:
        return min_n
    elif n > max_n:
        return max_n
    else:
        return n
