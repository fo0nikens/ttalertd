#! /usr/bin/python3
# James Loye Colley
from subprocess import Popen, PIPE


def who_is():
    w = Popen(['who'], stdout=PIPE).communicate()[0].decode().split()
    return [j for i, j in enumerate(w) if i % 5 == 0]


if __name__ == "__main__":
    users = who_is()
