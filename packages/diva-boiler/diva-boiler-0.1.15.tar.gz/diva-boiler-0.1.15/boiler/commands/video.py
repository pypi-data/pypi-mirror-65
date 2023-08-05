from collections import defaultdict
from pathlib import Path
import re
import sys
from typing import Dict
from uuid import UUID

import attr
import boto3
import click
from ffprobe import FFProbe

from boiler import BoilerSession, cli
from boiler.commands.utils import exit_with, handle_request_error
from boiler.definitions import CameraLocation, ReleaseBatches, Scenarios

video_name_regexp = re.compile(
    r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
    r'\.(?P<start_hour>\d{2})-(?P<start_minute>\d{2})-(?P<start_second>\d{2})'
    r'\.(?P<end_hour>\d{2})-(?P<end_minute>\d{2})-(?P<end_second>\d{2})'
    r'\.(?P<location>[^.]+)'
    r'\.(?P<gtag>G[^.]+)$'
)
BUCKET = 'diva-mturk-ingestion-prod'


def bold(x, **kwargs):
    return click.style(x, bold=True, **kwargs)


@attr.s(auto_attribs=True)
class VideoInfo:
    frame_rate: float
    duration: float
    width: int
    height: int
    name: str

    @classmethod
    def create(cls, file: str) -> 'VideoInfo':
        probe = FFProbe(file)
        stream = probe.streams[0]
        return cls(
            frame_rate=stream.framerate,
            duration=float(stream.duration),
            width=int(stream.width),
            height=int(stream.height),
            name=str(Path(file).stem),
        )

    def s3_path(self, id: UUID) -> str:
        _m = video_name_regexp.match(self.name)
        if _m is None:
            raise Exception('Could not parse video name')
        m = _m.groupdict()
        date = f'{m["year"]}-{m["month"]}-{m["day"]}'
        time = (
            f'{m["start_hour"]}-{m["start_minute"]}-{m["start_second"]}'
            f'{m["end_hour"]}-{m["end_minute"]}-{m["end_second"]}'
        )
        return f'uuid-encoded/{date}/{time}/{m["gtag"]}_{m["location"]}/{id}.mp4'


def ingest_video(video_path: str, release_batch: str, session: BoilerSession):
    video_name = Path(video_path).stem
    # until we fix the lambda, transcoding needs to be done manually:
    # ffmpeg -i <input> -f lavfi -i anullsrc -c:a aac -shortest -threads 12 \
    #        -c:v h264 -profile high <output>.avi

    if Path(video_path).suffix != '.mp4':
        raise Exception('Expected a transcoded video')

    r = session.get('video', json={'name': video_name})
    out = handle_request_error(r)
    if not r.ok:
        raise Exception(f'Could not query server for video={video_name}')

    if len(out['response']):
        video_id = out['response'][0]['id']
        click.echo(f'name={video_name} already exists', err=True)
    else:
        post_data = {'video_name': video_name, 'release_batch': release_batch}
        r = session.post('video/name', json=post_data)
        if not r.ok:
            raise Exception(f'Could not generate new video entity for {video_name}')
        video_id = r.json()['id']

    click.echo(f'id={video_id} created for name={video_name}', err=True)
    click.echo(f'sending name={video_name} id={video_id} to S3', err=True)

    s3 = boto3.client('s3')
    info = VideoInfo.create(video_path)
    try:
        s3.upload_file(video_path, BUCKET, info.s3_path(video_id))
    except Exception:
        click.echo('Could not upload file to S3.  Have you set up your credentials?', err=True)
        raise

    patch_data = {
        'duration': info.duration,
        'frame_rate': info.frame_rate,
        'height': info.height,
        'width': info.width,
    }
    resp = session.patch(f'video/{video_id}', json=patch_data)
    if not resp.ok:
        raise Exception(f'Could not set video metadata on {video_path}')


@click.group(name='video', short_help='ingest and query video')
@click.pass_obj
def video(ctx):
    pass


@video.command(name='status', help='status of video annotation')
@click.argument('name', type=click.STRING)
@click.pass_obj
def status(ctx, name):
    r = ctx['session'].get('video', params={'name': name})
    if not r.ok and r.status_code != 404:
        exit_with(handle_request_error(r))
    elif r.status_code == 404 or not r.json():
        click.echo('Video not found, has it been ingested?', err=True)
        sys.exit(1)

    video_id = r.json()[0]['id']
    r = ctx['session'].get(f'video/{video_id}/status').json()

    click.echo('-' * len(name))
    click.secho(name, bold=True)
    click.echo('-' * len(name))
    click.echo(f'https://admin.stumpf.avidannotations.com/#/video/{video_id}')

    status = r['status']
    fg = 'red'
    if 'complete' in status:
        fg = 'green'
    click.echo(f'status: {bold(status, fg=fg)}')
    click.echo(f"activity types: {bold(str(r['activity_type_count']))}")
    for cauldron in r['cauldrons']:
        click.echo(f"\ncauldron: {bold(cauldron['path'])}")
        click.echo(f"  * vendor: {bold(cauldron['vendor'])}")
        click.echo(f"  * set: {bold(cauldron['set_name'])}")

    total = 0
    total_counts: Dict[str, int] = defaultdict(lambda: 0)
    activities: Dict[str, Dict[str, int]] = defaultdict(lambda: {})
    for a in r['activity_types']:
        total += a['count']
        total_counts[a['activity_type']] += a['count']
        activities[a['activity_type']][a['status']] = a['count']

    click.echo(f'\n{total} activities:')
    for name in sorted(activities.keys()):
        summary = activities[name]
        fg = 'green' if summary.get('good') == total_counts[name] else 'yellow'

        click.echo(f'  * {bold(name, fg=fg)} ({total_counts[name]})')
        for status in sorted(summary.keys()):
            if status == 'good':
                continue
            count = summary[status]
            click.echo(f'    * {status} ({count})')


@video.command(name='search', help='search for video')
@click.option('--name', type=click.STRING)
@click.option('--gtag', type=click.STRING)
@click.option('--location', type=click.Choice([e.value for e in CameraLocation]))
@click.option('--release-batch', type=click.Choice([e.value for e in ReleaseBatches]))
@click.option('--scenario', type=click.Choice([e.value for e in Scenarios]))
@click.option('--phase', type=click.STRING)
@click.option('--page', type=click.INT)
@click.option('--size', type=click.INT)
@click.pass_obj
def search(ctx, **kwargs):
    data = {}
    for key, value in kwargs.items():
        if value is not None:
            data[key] = value
    r = ctx['session'].get('video', params=data)
    exit_with(handle_request_error(r))


@video.command(name='add', short_help='ingest video into stumpf from file')
@click.argument(
    'videos',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    nargs=-1,
    required=True,
)
@click.option(
    '--release-batch', type=click.Choice([e.value for e in ReleaseBatches]), required=True
)
@click.pass_obj
def add(ctx, videos, release_batch):
    """Ingest locally transcoded video files into Stumpf.

    \b
    Reference encoding settings are as follows:
        ffmpeg -i <input> -f lavfi -i anullsrc -c:a aac -shortest \\
               -c:v h264 -profile high <output>.avi

    This command requires a working `ffprobe` in your path.
    """
    for video in videos:
        ingest_video(video, release_batch, ctx['session'])


cli.add_command(video)
