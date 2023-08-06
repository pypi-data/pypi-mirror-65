
from time import sleep
from shutil import rmtree

from pyux.demo.interact import user_yes
from pyux.console import ColourPen
from pyux.logging import init_logger


def demo_logger():
    pen = ColourPen()
    print("""
    A log file will be created in './tmp' with name demo_run_time-of-run.log.
    By default, the logger writes to file and
    to console (which can be coloured).""")
    logger = init_logger(folder='./tmp', filename='demo', run_name='run')
    sleep(5)
    logger.info('An info message without color.')
    sleep(1)
    pen.write(style='bright', color='red', newline=False)
    logger.critical(
        'A critical message colored in bright red (in console only).')
    pen.write(
        message="\n\tA log file was created in './tmp'." +
                "Do you want to delete that folder ?",
        style='reset_all', newline=True
    )
    if user_yes(skip_char='k', action='keep'):
        rmtree('./tmp')
        print("    ./tmp folder deleted !")
