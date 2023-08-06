import random


DESCRIPTION = 'Find missed element of the progression'
PROGRESSION_LIMIT = 9


def make_progression():
    result = []
    first_num = random.randint(0, 10)
    result.append(first_num)
    k = random.randint(1, 10)
    for i in range(PROGRESSION_LIMIT):
        result.append(result[i] + k)
    return result


def make_question():
    progression = make_progression()
    index = random.randint(0, 9)
    symb_to_hide = progression[index]
    question = progression.copy()
    question[question.index(symb_to_hide)] = '..'

    return str(question), str(progression[index])
