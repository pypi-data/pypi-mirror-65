from pyux.time import Chronos, Timer, timeout, wait
from time import sleep


def demo_timer():
    print("\n    Use Timer to make a program wait and see where it is at.")
    Timer(delay=5, message="This is an example of a 5 seconds timer")
    print("""
    You can use also it for each iteration in a loop by decorating
    the iterable in a for statement.
    Here for a three iterations loop, pausing 3 seconds each time,
    and rewriting on the same line in terminal for each iteration
    (useful for big loops).
    """)
    sleep(8)
    for _ in Timer(3, delay=3, pattern='iteration : ', overwrite=True):
        pass


def demo_wait():
    print("""
    Use wait as a decorator to delay the execution of a function by a given
    amount of time. Pause can be made before or after actual call
    to the function. Here we decorate a simple print function with a 2s pause
    after execution.
    """)
    sleep(5)

    @wait(delay=2)
    def simple_print(message):
        print(message)

    simple_print("Print 'hello' then wait for two seconds.")
    simple_print("Say 'goodbye' then wait for two seconds.")
    simple_print('Finished !')

    print("""
    A timer can be printed instead of just using sleep
    """)
    sleep(2)

    @wait(delay=3, timer=True, message="A timer is printed before call")
    def simple_run():
        print('A function is executed.')

    simple_run()


def demo_timeout():
    print("""
    Use timeout as a decorator to make a function stop after a given time
    of execution. This is particularly useful to close infinite calls such
    as real-time API listeners within your code.

    Any exception raised by the decorated function will be raised. Timeout
    revolves on ``threading.Thread``, so a specific ``TimeoutThreadError``
    will be raised if the thread cannot be started.""")
    sleep(10)

    print("""
    Here we run a five seconds function with a three seconds timeout delay...
    """)
    sleep(2)

    @timeout(delay=3)
    def too_long():
        sleep(5)

    try:
        too_long()
    except TimeoutError as e:
        print('A TimeoutError was raised : %s' % e)


def demo_chronos():
    print("""
    Use Chronos to time stages of your script.
    You can also use it to time iterations within loops by decorating
    the iterable in the for statement.
    Here for a three iterations loop, with a pause equal to the iteration
    value.""")
    sleep(10)
    for _ in Chronos(range(1, 4), console_print=True):
        Timer(
            delay=_,
            message="Iteration %d, waiting %d secs" % (_, _),
            overwrite=True
        )
    sleep(3)
