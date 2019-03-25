#! /usr/bin/python3
# James Loye Colley
import logging


class log:
    def __init__(self):
        self.path = 'utils/ttalertd.log'

    def log_error(self, log_message):
        logging.basicConfig(
            filemode="a",
            format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
            datefmt="%Y-%m-%d-%H:%M%:%S",
            filename=self.path,
            level=logging.ERROR
        )
        logging.error(log_message)

    def log_critical(self, log_message):
        logging.basicConfig(
            filemode="a",
            format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
            datefmt="%Y-%m-%d-%H:%M:%S",
            filename=self.path,
            level=logging.CRITICAL
        )
        logging.critical(log_message)

    def log_info(self, log_message):
        logging.basicConfig(
            filemode="a",
            format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
            datefmt="%Y-%m-%d-%H:%M:%S",
            filename=self.path,
            level=logging.INFO
        )
        logging.info(log_message)
