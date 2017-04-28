from processor import Processor

class StdoutOutput(Processor):

    def __init__(self, config):
        self.config = config

    def run(self, line):
        if line:
            print line

        return line

