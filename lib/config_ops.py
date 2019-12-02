# -*- coding: utf-8 -*-
"""
    parser_factory to parse annotations of various datasets.

    Author : NoUnique (kofmap@gmail.com)
    Copyright (c) 2019. All Rights Reserved by NoUnique.
"""

import os
import glob
from yacs.config import CfgNode

_YAML_EXTS = {'.yml', '.yaml'}


def load_config(config=None, default='default'):
    conf_dir = os.path.abspath(os.path.join(__file__,
                                            os.path.pardir,
                                            os.path.pardir,
                                            'configs'))

    cfg_paths = {}
    for ext in _YAML_EXTS:
        for file_path in glob.glob(os.path.join(conf_dir, '*{}'.format(ext))):
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            cfg_paths[file_name] = file_path

    if default not in cfg_paths or not os.path.isfile(cfg_paths[default]):
        raise ValueError("Default configuration file does not exists : {}".format(default))
    # load default config
    conf = CfgNode.load_cfg(open(cfg_paths[default]))

    # load custom config and combine
    if config:
        if config not in cfg_paths or not os.path.isfile(cfg_paths[config]):
            raise ValueError("Invalid configuration, not exists : {}".format(config))
        conf.merge_from_file(cfg_paths[config])
    return conf


if __name__ == '__main__':
    cfg = load_config('kinetics400')
    print(cfg)
