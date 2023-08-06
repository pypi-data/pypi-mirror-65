import random


DESCRIPTION = 'What is the result of the expression?'


def make_question():
    num1, num2 = random.randint(0, 10), random.randint(0, 10)
    operations = {
        'sum': ('{} + {}'.format(num1, num2), str(num1 + num2)),
        'diff': ('{} - {}'.format(num1, num2), str(num1 - num2)),
        'mult': ('{} * {}'.format(num1, num2), str(num1 * num2)),
    }
    question, answer = random.choice(list(operations.values()))
    return question, answer