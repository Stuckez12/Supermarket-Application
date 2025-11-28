import logging


class UnableToFetchDataDBException(Exception):
    def __init__(self, messages: list[str]):
        for message in messages:
            logging.critical(message)

        super().__init__("Unable to fetch data")
