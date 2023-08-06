from pyux.console import ColourPen

pen = ColourPen()


def user_yes(skip_char='p', action='pass'):
    global pen
    pen.write(color='white', style='dim')
    text = input(
        '    Type any key to continue or %s to %s : ' %
        (skip_char, action)
    )
    pen.write(style='reset_all')
    return False if text == skip_char else True


def user_exit():
    global pen
    pen.write(
        '\n    Do you want to continue the demo ?',
        color='red', newline=True, reset=True
    )
    if not user_yes(skip_char='q', action='quit'):
        print('\n    Goodbye !')
        exit(0)
    else:
        return
