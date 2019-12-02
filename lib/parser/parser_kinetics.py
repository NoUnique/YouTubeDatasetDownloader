# -*- coding: utf-8 -*-
"""
    parser_factory to parse annotations of various datasets.

    Author : NoUnique (kofmap@gmail.com)
    Copyright (c) 2019. All Rights Reserved by NoUnique.
"""

from lib.parser.parser_base import Parser


class KineticsParser(Parser):
    def _parse_annotation(self, annotation_path):
        annotations = set()
        if self.annotation_type == 'csv':
            with open(annotation_path, 'r') as f:
                reader = self.lib.reader(f, delimiter=',')
                column_title = next(reader)
                for row in reader:
                    if len(column_title) == 5:
                        label, video_id, start_time, end_time, subset = row
                    elif len(column_title) == 4:
                        video_id, start_time, end_time, subset = row
                    annotations.add((video_id, start_time, end_time))
        elif self.annotation_type == 'json':
            pass
        else:
            pass
        return annotations
