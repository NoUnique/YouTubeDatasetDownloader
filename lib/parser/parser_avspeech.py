# -*- coding: utf-8 -*-
"""
    AVSpeech dataset parser.

    Author : OhJoon Kwon (ohjoon.kwon@samsung.com)
"""

from lib.parser.parser_base import Parser


class AVSpeechParser(Parser):
    def _parse_annotation(self, annotation_path):
        annotations = set()
        if self.annotation_type == 'csv':
            with open(annotation_path, 'r') as f:
                reader = self.lib.reader(f, delimiter=',')
                column_title = next(reader)
                for row in reader:
                    if len(column_title) == 5:
                        video_id, start_time, end_time, x_coordinate, y_coordinate = row
                    elif len(column_title) == 4:
                        print("Incomplete row")
                        continue
                        video_id, start_time, end_time, subset = row
                    annotations.add((video_id, start_time, end_time))
        elif self.annotation_type == 'json':
            pass
        else:
            pass
        return annotations
