import sys
from processor import Processor

class FifoInput(Processor):

    def __init__(self, config):
        super(FifoInput, self).__init__(config)
        try:
            fifo_path = self.config.get('fifo_path')
            self.fifo = open(fifo_path)
        except IOError:
            sys.exit('Error opening FIFO: {}'.format(fifo_path))

    def run(self, _line):
        return self.fifo.readline()

class StdinInput(Processor):

    def run(self, _line):
        return sys.stdin.readline()
