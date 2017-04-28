import json
import sys

DEFAULT_CONFIG_FILE_PATH = 'config_dev.json'

def load_config():
    config = {
        'processor_pipeline': [
            {'FifoInput': { 'fifo_path': 'test_fifo' }},
            {'StripNewLine': None},
            {'DecayingDedupFilter': {'ttl_seconds': '5', 'match': '^(echo)'} },
            {'StdoutOutput': None},
        ]
    }

    return config


def load_config_from_file(path=None):

    if path is None:
        path = DEFAULT_CONFIG_FILE_PATH

    try:
        with open(path) as config_file:
            return json.load(config_file)
    except IOError:
        sys.exit('Error loading config file: {}'.format(path))
    except ValueError:
        sys.exit('Error parsing config file: {}'.format(path))
