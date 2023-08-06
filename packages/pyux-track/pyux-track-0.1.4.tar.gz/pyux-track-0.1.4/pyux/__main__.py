
from pyux.console import ColourPen

from pyux.demo.messages import welcome
from pyux.demo.messages import intro
from pyux.demo.messages import goodbye
from pyux.demo.messages import messages
from pyux.demo.write import write_module


def main():
    pen = ColourPen()
    pen\
        .write(
            message=welcome, style='bright', color='cyan',
            newline=True, reset=True
        )\
        .write(message=intro, newline=True)

    for module_texts in messages.values():
        write_module(module_messages=module_texts)

    pen\
        .write(goodbye, color='yellow')\
        .close()


if __name__ == '__main__':
    main()
