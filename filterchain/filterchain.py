#!/bin/python

from config import load_config, load_config_from_file
from pipeline import build_pipeline, run_pipeline

def run():
    config = load_config_from_file()
    pipeline = build_pipeline(config)
    run_pipeline(pipeline)


if __name__ == '__main__':
    run()
