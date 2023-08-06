import random
from math import sqrt, ceil


DESCRIPTION = 'Answer "yes" if given number is prime. Otherwise answer "no"'


def make_question():
    rand_num = random.randint(1, 100)
    return str(rand_num), correct_answer(rand_num)


def is_prime(num):
    lim = ceil(sqrt(num))
    for i in range(2, lim):
        if (num % i) == 0:
            return False
    return True


def correct_answer(num):
    if is_prime(num):
        return 'yes'
    return 'no'
