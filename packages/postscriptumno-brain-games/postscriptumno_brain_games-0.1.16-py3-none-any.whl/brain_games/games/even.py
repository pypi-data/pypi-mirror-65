import random


DESCRIPTION = 'Answer "yes" if number even otherwise answer "no".'


def make_question():
    rand_num = random.randint(1, 100)
    return str(rand_num), correct_answer(rand_num)


def correct_answer(num):
    if num % 2 == 0:
        return 'yes'
    return 'no'
