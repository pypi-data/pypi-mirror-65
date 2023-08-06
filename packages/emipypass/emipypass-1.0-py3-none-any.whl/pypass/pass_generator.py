import string
import random
def digit_pass(len):
    return "".join(random.choices(string.digits, k=len))
def strong_pass(len):
    return "".join(random.choices(string.digits + string.ascii_letters, k=len))
