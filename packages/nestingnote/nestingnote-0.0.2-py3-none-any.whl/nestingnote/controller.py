from nestingnote.commands import Commands
from nestingnote.model import Model


class Controller(object):

    def __init__(self, model: Model):
        self.model = model

    def __input_stream(self):
        """Main loop, waiting on keyboard input"""
        while True:
            self.model.display()
            key: int = self.model.input_char
            Commands.execute(key, self.model)

    def run(self):
        """
        Must be called after instantiation
        Continue running the TUI until interruption
        """
        try:
            self.__input_stream()
        except KeyboardInterrupt:
            pass
