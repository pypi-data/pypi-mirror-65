#!/usr/bin/env python3

import argparse

from .model import DHEConfiguration
from .core import calc, save_result_csv


def calc_from_file(config_file, out_file):
    cfg = DHEConfiguration.load(config_file)
    result = calc(cfg)
    save_result_csv(result, out_file)


def run():
    parser = argparse.ArgumentParser(description="DHE")
    parser.add_argument("-o", dest="out", default=None,
                        help="Output file (default: <input file>.npy )")
    parser.add_argument("config", help="Config file")
    cmd_args = parser.parse_args()
    out = cmd_args.out
    if out is None:
        out = cmd_args.config.split(".", 1)[0] + ".npy"
    calc_from_file(cmd_args.config, out_file=out)


if __name__ == '__main__':
    run()
