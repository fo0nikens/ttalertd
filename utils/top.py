#! /usr/bin/python3
# James Loye Colley
# get system data from top: load averages, number of users,
# and top processes' PID, USER, CPU%, and Command Path
from os import popen
from itertools import chain


class Top:
    def __init__(self):
        self.general_sys_info = {
            'number_of_users': '',
            'load_averages': []
        }
        self.process = {
            'pid': '',
            'user': '',
            'cpu_percentage': '',
            'name': ''
        }

    @staticmethod
    def __start_process():
        for line in popen('top -n 1 -cb | head -15'):
            if len(line.split()) != 0:
                yield line.split()

    def run_top(self):
        first_elements = ['Tasks:', '%Cpu(s):', 'KiB', 'PID']
        for line_list in self.__start_process():
            if line_list[0] not in first_elements:
                if line_list[0] != 'top':
                    self.process['pid'] = line_list[0]
                    self.process['user'] = line_list[1]
                    self.process['cpu_percentage'] = line_list[8]
                    yield self.process
                else:
                    if not line_list[5].isdigit():
                        self.general_sys_info['number_of_users'] = line_list[6]
                    else:
                        self.general_sys_info['number_of_users'] = line_list[5]
                    if line_list[9] != 'average:':
                        avgs = line_list[9:]
                    else:
                        avgs = line_list[10:]
                    self.general_sys_info['load_averages'] = [x.replace(',', '') for x in avgs]
                    yield self.general_sys_info


if __name__ == "__main__":
    for k, v in enumerate(chain.from_iterable(i.items() for i in Top().run_top())):
        if k < 2 or 'name' in v:
            print("%s: %s\n" % (v[0],  v[1]))
        else:
            print("%s: %s" % (v[0], v[1]))
