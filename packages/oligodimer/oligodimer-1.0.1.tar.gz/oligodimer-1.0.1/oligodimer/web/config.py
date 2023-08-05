#!/usr/bin/env python3

'''OligoDimer: Detecting dimers among multiple oligo sequences
Github: https://github.com/billzt/OligoDimer
This is a CLI script to configure OligoDimer
'''

import argparse
import os
import sys
import json

def load():
    home_dir = os.environ['HOME']
    web_config = json.load(open(f'{home_dir}/.oligodimer.json'))
    return web_config

def prepare():
    home_dir = os.environ['HOME']
    if os.path.isfile(f'{home_dir}/.oligodimer.json') is False:
        os.system(f"cp {os.path.dirname(__file__)}/web_config_sample.json {home_dir}/.oligodimer.json")
    print(f'Configure file {home_dir}/.oligodimer.json is ready. Please modify it')

def check():
    home_dir = os.environ['HOME']
    if os.path.isfile(f'{home_dir}/.oligodimer.json') is False:
        return({'status':'error', 'msg':'OligoDimer has not been configured yet. Please run oligodimer-cfg to configure it'})
    else:
        return({'status':'success', 'msg':'Success!'})

if __name__ == "__main__":
    print(json.dumps(prepare()))
