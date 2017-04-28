from processor import Processor

class StripNewLine(Processor):

    def run(self, line):
        return line.strip()

