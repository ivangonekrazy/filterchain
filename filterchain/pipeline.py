import processors
import sys

def build_pipeline(config):
    try:
        processors_class_and_config = [
            (getattr(processors, p.keys()[0]), p.values()[0])
            for p in config['processor_pipeline']
        ]
    except AttributeError:
        sys.exit('Error building pipeline. Please check configuration.')

    return [ _class(_config) for _class, _config in processors_class_and_config ]


def run_pipeline(pipeline):

    try:
        while True:
            line = None
            for processor in pipeline:
                line = processor.run(line)
                if line is None:
                    break
    except KeyboardInterrupt:
        sys.exit(0)
