#!/usr/bin/env python3


import ffmpeg


def get_codecs(fname):
    probe = ffmpeg.probe(fname)
    video_codec, audio_codec = None, None
    for stream in probe['streams']:
        stream_type = stream['codec_type']
        if stream_type == 'video':
            video_codec = stream['codec_name']
        elif stream_type == 'audio':
            audio_codec = stream['codec_name']
        if video_codec and audio_codec:
            break
    return video_codec, audio_codec


if __name__ == '__main__':
    test = '/array/mark/videos/chromium-test.webm'
    print(get_codecs(test))
