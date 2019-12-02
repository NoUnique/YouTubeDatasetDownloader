# -*- coding: utf-8 -*-
"""
    base parser class

    Author : NoUnique (kofmap@gmail.com)
    Copyright (c) 2019. All Rights Reserved by NoUnique.
"""

import importlib
from abc import ABC, abstractmethod

supported_types = ['csv', 'json']


class Parser(ABC):
    def __init__(self, annotation_type, **kwargs):
        super(Parser, self).__init__(**kwargs)
        if annotation_type not in supported_types:
            raise ValueError('Not supported annotation type')
        self.annotation_type = annotation_type
        self.lib = importlib.import_module(annotation_type)

    @abstractmethod
    def _parse_annotation(self, annotation_filepath):
        pass

    def parse_annotations(self, annotation_paths):
        download_list = set()
        for annotation_path in annotation_paths:
            download_list.update(self._parse_annotation(annotation_path))
        return download_list
