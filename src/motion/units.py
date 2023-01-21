from math import round


def marlinFormat(input_float: float):
    """Round a given input float to four decimal points for Marlin return needs."""
    return round(input_float, 4)
