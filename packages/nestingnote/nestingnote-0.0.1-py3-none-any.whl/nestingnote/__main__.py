#!/usr/bin/python3
from model import Model
from linuxView import LinuxView
from curses import wrapper
from controller import Controller
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
