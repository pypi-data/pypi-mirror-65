from time import sleep

from pyux.console import ColourPen, Speak, Wheel, wordy, ProgressBar


def demo_wheel():
    print("""
    You can print the number of iterations, here for 30 iterations""")
    for _ in Wheel(30):
        sleep(0.1)
    print("""
    Or the iterated value, here for an iteration over 30 paths""")
    sleep(2)
    paths = ['fakepath_%d' % index for index in range(30)]
    for _ in Wheel(paths, print_value=True):
        sleep(0.1)


def demo_speak():
    print("""
        Use Speak to decorate an iterable and print a message after each
        iteration, or after a given number of iterations. Here, a dot is
        printed each 10 iterations, among 50.""")
    for _ in Speak(50, every=10):
        sleep(0.1)


def demo_wordy():
    print("""
    wordy decorates a function to print a message at each function call.
    When catch = True, if the call raises an exception, it is returned as the
    function response and a specific message is printed.
    Messages can be colored.

    Here with default values : a dot for success and an exclamation mark
    for failure, on a function that raises an error if its argument is 4 or 8.
    """)
    sleep(5)
    @wordy(catch=True, colors=('GREEN', 'RED'))
    def error_4(value):
        if value in (4, 8):
            raise ValueError
        return

    for x in range(10):
        sleep(1)
        error_4(x)
    print('')


def demo_progress():
    print("""
    You can print a progress bar that will adjust to the window size,
    here for 2 500 iterations""")
    for _ in ProgressBar(2500):
        sleep(0.001)


def demo_pen():
    pen = ColourPen()
    print('\n\tYou can set colour and styles among predefined values :')
    pen\
        .write(message='\tThis is red', color='red', newline=True)\
        .write(
            message='\tThis is blue', color='cyan', style='bright',
            newline=True
        )\
        .write(reset=True)

    pen\
        .write('    You can also', color='green')\
        .write(' change colors within', color='magenta')\
        .write(' the same line!', color='yellow', reset=True, newline=True)
