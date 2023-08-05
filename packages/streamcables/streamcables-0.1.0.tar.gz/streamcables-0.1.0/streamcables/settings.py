# settings.py

import logging
from shutil import copyfile

import toml
from appdirs import AppDirs

config = {}

import os


def init():
    global config
    config = {'dirs': AppDirs("StreamCables", "NoNoTools")}

    config['settings_fn'] = config['dirs'].user_data_dir + "/settings.toml"
    try:
        config = {**config, **toml.load(config['settings_fn'])}
        print('Reading ' + config['settings_fn'] + '...')
    except FileNotFoundError:
        logging.warning("Edit " + config['settings_fn'] + '!')
        src = os.path.dirname(os.path.realpath('../settings.default.toml'))
        copyfile(src, config['settings_fn'])
        exit(1)
