#!/usr/bin/env python3


import ffmpeg
import subprocess as sub
import os


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
    vcodec, acodec = convert_to_ffmpeg_args(*get_codecs(fname))
    path, _ = os.path.splitext(fname)
    outname = f"{path}.webm"
    if vcodec != "copy" or acodec != "copy":
        cmd = f"ffmpeg -i {fname} -vcodec {vcodec} -acodec {acodec} {outname}"
    stdout = sub.check_output(cmd, shell=True)
    return stdout


def mark_for_deletion(fname):
    '''
    Moves a file to an in-place archive directory for future deletion.
    '''
    directory = os.dirname(os.path.abspath(fname))
    archive_dir = 'archive'
    try:
        os.mkdir(os.path.join(directory, archive_dir))
    except FileExistsError:
        pass
    outname = os.path.join(directory, archive_dir, os.path.basename(fname))
    os.rename(fname, outname)


def get_targets(dirname):
    files = os.listdir(dirname)
    files = list(map(lambda f: os.path.join(dirname, f), files))
    files = [f for f in files if os.path.isfile(f)]
    return files


def main(dirname):
    targets = get_targets(dirname)
    for f in targets:
        try:
            transcode(f)
            mark_for_deletion(f)
        except ffmpeg._run.Error:
            continue


if __name__ == '__main__':
    target_dirs = ['/array/mark/videos']
    for d in target_dirs:
        main(d)
