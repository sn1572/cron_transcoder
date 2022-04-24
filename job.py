#!/usr/bin/env python3


import ffmpeg
import subprocess as sub


def convert_to_ffmpeg_args(video_codec, audio_codec):
    if video_codec == 'vp8':
        out_video_codec = 'copy'
    else:
        out_video_codec = 'vp8'
    if audio_codec == 'opus':
        out_audio_codec = 'copy'
    else:
        out_audio_codec = 'libopus'
    return out_video_codec, out_audio_codec


def get_codecs(fname):
    '''
    Returns the video and audio codec arguments to ffmpeg
    for a given video file.
    '''
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


def transcode(fname):
    vcodec, acodec = convert_to_ffmpeg_args(*get_codecs(test))
    path, _ = os.path.splitext(fname)
    outname = f"{path}.webm"
    if vcodec != "copy" and acodec != "copy":
        cmd = f"ffmpeg -i {fname} -vcodec {vcodec} -acodec {acodec} {outname}"
    stdout = sub.check_output(cmd, shell=True)


if __name__ == '__main__':
    test = '/array/mark/videos/chromium-test.webm'
