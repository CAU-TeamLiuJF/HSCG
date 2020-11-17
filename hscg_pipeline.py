#! /bin/env python

import os
import argparse
import time

from hscg.pipeline import generate_custom_config, read_and_run_custom_config

# Need check necessary packages !!!!!!!!!!!!!!!!!!!!!!!!!!!!

description="""Genome Assembly Pipeline
Scaffolding options: PBJELLY2, SSPACELongRead
Gap Filling options: TGS_GapCloser, LR_Gapcloser"""

parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--config', action='store_true', default=False, help='Generate configuration files for assembly pipeline.')
parser.add_argument('--run', action='store_true', default=False, help='Running the assembly pipeline.')
# parser.add_argument('-l', '--log', type=str, default="pipeline.{}.log".format(time.strftime('%Y-%m-%d',time.localtime(time.time()))), help='Define the log file.')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.1')
args = parser.parse_args()


if args.config:
    print('OK, generate configuration.')
    generate_custom_config()
elif args.run:
    print('OK, run pipeline')
    read_and_run_custom_config()
    # print('Log file is in: ', args.log)

else:
    print("ERROR input, please see run_pipeline.py -h")
