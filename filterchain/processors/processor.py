class Processor(object):

    def __init__(self, config):
        self.config = config

    def run(self, line):
        raise NotImplementedError

