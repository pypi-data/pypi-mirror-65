#!/usr/bin/python3
from nestingnote.model import Model
from nestingnote.linuxView import LinuxView
from curses import wrapper
from nestingnote.controller import Controller
import sys
import os
from pathlib import Path


def main(window):
    file_path = get_file_path()
    view = LinuxView(window)
    model = Model(view, file_path)
    controller: Controller = Controller(model)
    controller.run()


def get_file_path():
    if len(sys.argv) < 2:
        home = str(Path.home())
        path = os.path.join(home, 'Documents', 'newNote.nnn')
        return add_unique_postfix(path)
    return sys.argv[1]


def add_unique_postfix(file_name):
    if not os.path.exists(file_name):
        return file_name
    path, name = os.path.split(file_name)
    name, ext = os.path.splitext(name)
    for i in range(1, 1000000):
        unique_filename = os.path.join(path, '%s(%d)%s' % (name, i, ext))
        if not os.path.exists(unique_filename):
            return unique_filename
    raise Exception("Out of default file names")


if __name__ == '__main__':
    wrapper(main)
