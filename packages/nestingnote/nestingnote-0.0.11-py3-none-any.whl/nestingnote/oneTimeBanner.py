class OneTimeBanner(object):
    def __init__(self):
        self.__message = None

    @property
    def has_message(self) -> bool:
        return self.__message is not None

    @property
    def message(self) -> str:
        to_return = self.__message
        self.__message = None
        return to_return

    @message.setter
    def message(self, new_message: str):
        self.__message = new_message

