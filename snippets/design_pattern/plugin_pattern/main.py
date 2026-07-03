from package.repository import execute, register


@register('cry')
def cry(sentence: str):
    """
    Docstring for cry

    :param sentence: Description
    :type sentence: str
    """
    return "I dont wan't to cry! " + sentence


def main():
    execute('Listen to uS', 'shout')
    execute('Hey', 'scream')
    execute('Well doNe', 'whisper')
    execute('Ahhh', 'cry')


if __name__ == '__main__':
    main()
