import datetime
import re
import sre_constants

from collections import Counter
from filterchain.exceptions import *
from processor import Processor

class DecayingDedupFilter(Processor):

    def __init__(self, config):
        super(DecayingDedupFilter, self).__init__(config)
        self.ttl_seconds = datetime.timedelta(seconds=int(config.get('ttl_seconds')))
        self.term_time = {}

        try:
            self.matcher = re.compile(self.config.get('match'), re.IGNORECASE)
        except sre_constants.error:
            raise ConfigurationError('Malformed regex for {} matcher.'.format(self.__class__))

    def run(self, line):
        match = self.matcher.match(line)

        if match:
            now = datetime.datetime.now()
            match_group = match.group(0)

            if match_group in self.term_time:
                if (now - self.term_time[match_group]) > self.ttl_seconds:
                    self.term_time[match_group] = now
                else:
                    return None
            else:
                self.term_time[match_group] = now

        return line


class RedactFilter(Processor):

    def __init__(self, config):
        super(RedactFilter, self).__init__(config)
        self.redaction_char = self.config.get('redaction_char', '#')

        try:
            self.matcher = re.compile(self.config.get('match'), re.IGNORECASE)
        except sre_constants.error:
            raise ConfigurationError('Malformed regex for {} matcher.'.format(self.__class__))

    def _replacer(self, match_obj):

        return len(match_obj.group(0)) * self.redaction_char

    def run(self, line):
        return self.matcher.sub(self._replacer, line)


class RemoveFilter(Processor):

    def __init__(self, config):
        super(RemoveFilter, self).__init__(config)

        try:
            self.matcher = re.compile(self.config.get('match'), re.IGNORECASE)
        except sre_constants.error:
            raise ConfigurationError('Malformed regex for {} matcher.'.format(self.__class__))

    def run(self, line):
        match = self.matcher.match(line)

        if match:
            return None

        return line


class TopNFilter(Processor):

    def __init__(self, config):
        super(TopNFilter, self).__init__(config)
        self.top_n = int(config.get('top_n'))
        self.counter = Counter()

    def run(self, line):
        self.counter[line] += 1

        if line in [l for l,_c in self.counter.most_common(self.top_n)]:
            return None

        return line
