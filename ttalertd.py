#! /usr/bin/python3
# James Loye Colley
from utils import Compare, Top, default_values, get_structure
from utils import read_data, write_data, who_is, files_exist
from utils import log
from itertools import chain
from threading import Thread
from time import sleep
from sys import exit


class TTAlertd:
    def __init__(self):
        self.new_data = []
        self.get_new_metrics()
        self.path = 'utils/memory.json'
        self.ALERT_INTERVAL = default_values()['ALERT_INTERVAL']
        self.RESET_INTERVAL = default_values()['RESET_INTERVAL']
        self.log = log()

    def get_existing_metrics(self):
        return read_data(self.path)

    def get_new_metrics(self):
        t = chain.from_iterable(i.items() for i in Top().run_top())
        new_data = [entry for entry in t]
        self.new_data = [tup[1] for tup in new_data]
        self.new_data.insert(0, sorted(who_is()))

    def compare_metrics(self):
        if read_data(self.path)['iterations'] >= self.RESET_INTERVAL:
            write_data(self.path, get_structure())
            m = "Reached RESET_INTERVAL %s" % str(self.RESET_INTERVAL)
            self.log.log_info(m)
        sleep(self.ALERT_INTERVAL)
        c = Compare(self.new_data, self.get_existing_metrics())
        c.compare()


if __name__ == "__main__":
    if not files_exist():
        m = "Ensure utils/memory.json & utils/credentials.yml exist"
        log = log()
        log.log_error(m)
        exit(1)
    ttalertd = TTAlertd()
    thread = Thread(target=ttalertd.compare_metrics)
    thread.start()
    thread.join()
