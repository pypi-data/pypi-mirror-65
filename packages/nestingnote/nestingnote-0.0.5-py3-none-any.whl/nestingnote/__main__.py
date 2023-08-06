#!/usr/bin/python3
from nestingnote.model import Model
from nestingnote.linuxView import LinuxView
from curses import wrapper
from nestingnote.controller import Controller
from sys import argv


def main(window):
    try:
        file_name = argv[1]
    except IndexError:
        raise Exception("Missing first argument: file name")
    view = LinuxView(window)
    model = Model(view, file_name)
    controller: Controller = Controller(model)
    controller.run()


if __name__ == '__main__':
    wrapper(main)
