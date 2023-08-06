from pyux.demo.interact import user_yes, user_exit
from pyux.console import ColourPen

TITLE_STYE = {'color': 'yellow', 'style': 'bright'}
DIV_STYLE = {'color': 'green', 'style': 'normal'}


def write_module(module_messages: dict) -> None:
    pen = ColourPen()
    pen\
        .write(
            message=module_messages['title'],
            color=TITLE_STYE['color'],
            style=TITLE_STYE['style'],
            reset=True
        )\
        .write(message=module_messages['intro'], newline=True)

    for div in module_messages['divs']:
        pen.write(
            message=div['text'],
            color=DIV_STYLE['color'],
            style=DIV_STYLE['style'],
            reset=True
        )
        if user_yes():
            div['fun']()
    user_exit()
