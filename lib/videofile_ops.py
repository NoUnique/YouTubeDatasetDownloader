# -*- coding: utf-8 -*-
"""
    parser_factory to parse annotations of various datasets.

    Author : NoUnique (kofmap@gmail.com)
    Copyright (c) 2019. All Rights Reserved by NoUnique.
"""

import os


def get_filename(video_id, start_time, end_time):
    file_format = 'mp4'
    filename_format = '{}_{:07.1f}_{:07.1f}.{}'
    return filename_format.format(video_id,
                                  float(start_time), float(end_time),
                                  file_format)


def get_output_filename(video_id, output_dir, start_time, end_time):
    filename = get_filename(video_id, start_time, end_time)
    output_filename = os.path.join(output_dir, filename)
    return output_filename


def drop_duplicates(annotations, output_dir):
    downloaded = list(map(os.path.basename, os.listdir(output_dir)))
    for annotation in annotations:
        if get_filename(*annotation) in downloaded:
            annotations.remove(annotation)
