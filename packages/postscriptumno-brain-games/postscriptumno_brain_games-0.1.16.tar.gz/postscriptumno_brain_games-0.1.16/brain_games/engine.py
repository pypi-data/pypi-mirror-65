import prompt


ROUNDS_NUM = 3


def greeting():
    print('Welcome to the Brain Games!')
    name = prompt.string('May I have your name? ')
    print('Hello, ' + name)
    return name


def compare_answers(correct_answer, user_answer):
    if correct_answer == user_answer:
        print('Correct')
        return True
    print('"{}" is wrong answer ;(. Correct answer was "{}"'.format(
            user_answer, correct_answer
        ))
    return False


def run(game):
    name = greeting()
    print(game.DESCRIPTION)

    for _ in range(ROUNDS_NUM):
        question, correct_answer = game.make_question()
        print('Question: ' + question)

        user_answer = prompt.string('Answer: ')
        if correct_answer == user_answer:
            print('Correct')
            continue
        else:
            print('"{}" is wrong answer ;(. Correct answer was "{}"'.format(
                user_answer, correct_answer
            ))
            print('Let\'s try again, {}'.format(name))
            return
    print('Congratulations, {}'.format(name))
