# my_py_rim_repo/utils/pi.py
import math


def get_pi_digit(n):
    digits = list(str(math.pi))
    digits.remove('.')
    return int(digits[n-1])

