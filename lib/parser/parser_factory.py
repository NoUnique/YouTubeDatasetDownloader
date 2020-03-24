# -*- coding: utf-8 -*-
"""
    parser_factory to parse annotations of various datasets.

    Author : NoUnique (kofmap@gmail.com)
    Copyright (c) 2019. All Rights Reserved by NoUnique.
"""

import functools

from lib.parser.parser_kinetics import KineticsParser
from lib.parser.parser_avspeech import AVSpeechParser

parser_map = {
    'kinetics': KineticsParser,
    'kinetics400': KineticsParser,
    'kinetics600': KineticsParser,
    'kinetics700': KineticsParser,
    'avspeech': AVSpeechParser,
}


def get_parser(name, annotation_type):
    if name not in parser_map.keys():
        raise ValueError('Not supported dataset: {}'.format(name))
    cls_obj = parser_map[name]
    @functools.wraps(annotation_type)
    @functools.wraps(cls_obj)
    def parser_fn(**kwargs):
        return cls_obj(annotation_type, **kwargs)
    return parser_fn()
