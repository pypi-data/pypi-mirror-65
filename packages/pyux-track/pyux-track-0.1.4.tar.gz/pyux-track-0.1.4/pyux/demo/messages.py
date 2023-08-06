from shutil import get_terminal_size

from pyux.demo.modules.console import demo_pen, demo_progress, demo_speak
from pyux.demo.modules.console import demo_wheel, demo_wordy
from pyux.demo.modules.time import demo_chronos, demo_timer
from pyux.demo.modules.time import demo_timeout, demo_wait
from pyux.demo.modules.logging import demo_logger

__WIDTH__ = get_terminal_size()[0]


def title_char(x):
    x = "\n===   %s   " % x
    x = x + '=' * (__WIDTH__ - len(x)) + '\n'
    return x


welcome = """%s
    Welcome to pyux tools demo
%s""" % ("=" * __WIDTH__, "=" * __WIDTH__)

intro = """
    All available tools in this package will now be demonstrated !
    Read the README to see the nitty gritty of using them."""

goodbye = """
    This demo has ended ! Thanks for using pyux and feel free to suggest
    improvements at https://gitlab.com/roamdam/pyux."""

messages = {
    "console": {   # title, intro and divs for module console
        "title": title_char('1. Module console'),
        "intro": """
    Classes available in console package help you with printing stuff
    when a script is running.""",
        "divs": [
            {
                'text': """
    Wheel : print a turning wheel within a for loop (or manually).
    The iteration counter or the iterated value is printed next to the wheel.
""",
                'fun': demo_wheel,
            },
            {
                'text': """
    Speak : print a message at each iteration within a loop.
""",
                'fun': demo_speak
            },
            {
                'text': """
    wordy : print a message at each function call.
""",
                'fun': demo_wordy
            },
            {
                'text': """
    ProgressBar : inspired by tqdm package, print a progress bar
    within a for loop (or manually).
""",
                'fun': demo_progress
            },
            {
                'text': """
    ColourPen : colourise and style text for terminal printing, with package
    colorama. This is what this demo uses to colour text !
""",
                'fun': demo_pen
            }
        ]
    },
    "time": {   # title, intro and divs for module time
        "title": title_char('2. Module time'),
        "intro": """
    Classes available in time package are relative to time in a script : either
    making it wait, or timing durations.""",
        "divs": [
            {
                'text': """
    Timer : print a timer for a given delay.
    A counter and a message can be printed too.
""",
                'fun':  demo_timer
            },
            {
                'text': """
    Chronos : a stopwatch for your script or your loops.
    Can save results in a tsv file.
""",
                'fun': demo_chronos
            },
            {
                'text': """
    wait : a decorator to make a function wait before or after execution.
""",
                'fun': demo_wait
            },
            {
                'text': """
    timeout : a decorator to make a function stop after a given time
    of execution.
""",
                'fun': demo_timeout
            }
        ]
    },
    "logging": {   # title, intro and divs for module logging
        "title": title_char('3. Module logging'),
        "intro": """
    The logging module contains only function init_logger, that you can use to
    initiate a logger instance. You can specify name and destination folder for
    the log file. By defaut, the name changes at each execution so it creates
    a different log file by execution. You can give your own logging.conf or
    use the default format included.""",
        "divs": [
            {
                'text': """
    init_logger : initiate a root logger that creates a different log file for
    each execution.
""",
                'fun': demo_logger
            }
        ]
    }
}
