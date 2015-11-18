from __future__ import print_function
import arrow

LOGFILE = "slack.log"

class Logger(object):
    def __init__(self, name):
        self._name = name
        with open(LOGFILE, "w") as f:
            f.write("")

    def info(self, msg):
        self.write("%s -- [%s:INFO] -- %s" % (arrow.now(), self._name, msg))

    def warn(self, msg):
        self.write("%s -- [%s:WARNING] -- %s" % (arrow.now(), self._name, msg))

    def error(self, msg):
        self.write("%s -- [%s:ERROR] -- %s" % (arrow.now(), self._name, msg))

    def write(self, msg):
        print(msg)
        with open(LOGFILE, "a") as f:
            f.write((msg.encode("utf-8")) + "\n")
