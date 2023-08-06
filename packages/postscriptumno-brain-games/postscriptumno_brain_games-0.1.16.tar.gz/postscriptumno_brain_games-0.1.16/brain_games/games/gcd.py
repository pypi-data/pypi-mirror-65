import random
from math import gcd


DESCRIPTION = 'Find greatest common divisor of two numbers'


def make_question():
    num1 = random.randint(0, 10)
    num2 = random.randint(0, 10)
    question = '{}, {}'.format(num1, num2)
    answer = str(gcd(num1, num2))
    return question, answer

def gcd(num1, num2):
    if not num2:
        return num1
    return gcd(num2, num1 % num2)