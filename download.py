# -*- coding: utf-8 -*-
"""
    parser_factory to parse annotations of various datasets.

    This script downloads and resize action recognition datasets
    Youtube-dl (https://github.com/ytdl-org/youtube-dl)
    FFMPEG (https://www.ffmpeg.org)

    Author : NoUnique (kofmap@gmail.com)
    Copyright (c) 2019. All Rights Reserved by NoUnique.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import subprocess

import argparse
import random
from multiprocessing import Pool
from functools import partial

from lib.youtube_ops import get_youtube_info
from lib.ffmpeg_ops import encode_video
from lib.videofile_ops import get_output_filename, drop_duplicates
from lib.parser.parser_factory import get_parser
from lib.config_ops import load_config


def download_clip(annotation, output_dir,
                  min_size=256, x264_preset='veryfast',
                  num_attempts=10, proxy=None):
    video_id, start_time, end_time = annotation

    status = False
    attempts = 0
    download_url = None
    width, height = (None, None)

    # get direct url using youtube-dl
    while True:
        try:
            download_url, width, height = get_youtube_info(video_id, proxy)
            break
        except Exception as err:
            attempts += 1
            if attempts == num_attempts:
                return status, err

    # set filename
    output_filename = get_output_filename(video_id, output_dir,
                                          start_time, end_time)

    # download video, resize, and encode it.
    try:
        encode_video(download_url, output_filename,
                     width, height, start_time, end_time,
                     x264_preset=x264_preset, resize=True, min_size=min_size)
    except subprocess.CalledProcessError as err:
        return status, err.output

    # check if the video was successfully saved.
    status = os.path.exists(output_filename)
    return status, 'Downloaded'


def main(cfg_name=None):
    cfg = load_config(cfg_name)
    if not os.path.isdir(cfg.OUTPUT_DIR):
        os.makedirs(cfg.OUTPUT_DIR)

    # Reading and parsing annotations.
    parser = get_parser(cfg.DATASET.NAME, cfg.DATASET.ANNOTATION.TYPE)
    annotations = parser.parse_annotations(cfg.DATASET.ANNOTATION.FILES)
    if cfg.DROP_DUPLICATES:
        annotations = drop_duplicates(annotations, cfg.OUTPUT_DIR)

    # Download all clips.
    if cfg.SHUFFLE:
        random.shuffle(annotations)
    if cfg.NUM_WORKERS > 1:
        pool = Pool(cfg.NUM_WORKERS)
        pool.map(partial(download_clip,
                         output_dir=cfg.OUTPUT_DIR,
                         min_size=cfg.MIN_SIZE,
                         x264_preset=cfg.X264_PRESET,
                         num_attempts=cfg.NUM_ATTEMPTS,
                         proxy=cfg.PROXY), annotations)
    else:
        for annotation in annotations:
            download_clip(annotation,
                          output_dir=cfg.OUTPUT_DIR,
                          min_size=cfg.MIN_SIZE,
                          x264_preset=cfg.X264_PRESET,
                          num_attempts=cfg.NUM_ATTEMPTS,
                          proxy=cfg.PROXY)


if __name__ == '__main__':
    description = 'Script for downloading and trimming various video datasets.'
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('--cfg', dest='cfg_name', type=str, default=None,
                            help='Location of config file.')
    args = arg_parser.parse_args()

    main(**vars(arg_parser.parse_args()))
