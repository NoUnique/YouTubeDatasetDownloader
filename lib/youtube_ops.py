# -*- coding: utf-8 -*-
"""
    parser_factory to parse annotations of various datasets.

    Author : NoUnique (kofmap@gmail.com)
    Copyright (c) 2019. All Rights Reserved by NoUnique.
"""

import youtube_dl

_URL_FORMAT = 'https://www.youtube.com/watch?v={}'
_TARGET_FORMAT_ID = 18


def get_youtube_info(video_id):
    assert isinstance(video_id, str), "video_id must be string"
    assert len(video_id) == 11, 'video_identifier must have length 11'

    target_url = _URL_FORMAT.format(video_id)

    with youtube_dl.YoutubeDL(dict(forceurl=True)) as ydl:
        resp = ydl.extract_info(target_url, download=False)
        infos = resp['formats']
        for info in infos:
            # 18 - 360p or 240p h264 encoded video (with audio)
            if info['format_id'] == '18':
                return info['url'], info['width'], info['height']
        raise youtube_dl.DownloadError('There is no format_id=={}'.format(_TARGET_FORMAT_ID))
