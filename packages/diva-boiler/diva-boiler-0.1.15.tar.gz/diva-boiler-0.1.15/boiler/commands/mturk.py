import locale
from typing import NamedTuple

import click
from requests import Session
from tabulate import tabulate

from boiler import cli

locale.setlocale(locale.LC_ALL, '')


class CostStatistics(NamedTuple):
    count: int  # type: ignore
    total: float
    p50: float
    p90: float
    p95: float
    p99: float
    average: float


def mturk_costs(session: Session) -> CostStatistics:
    resp = session.get('mturk/cost')
    return CostStatistics(**resp.json())


def mturk_balance(session: Session) -> float:
    resp = session.get('mturk/balance')
    if not resp.ok:
        click.secho('Could not get mechanical turk balance.', fg='red')
        return 0
    return resp.json()


@click.group(name='mturk', short_help='Get information about HITs on mechanical turk')
def mturk():
    pass


@mturk.command(help='Get the available balance in our account')
@click.pass_obj
def balance(ctx):
    b = mturk_balance(ctx['session'])
    click.echo(locale.currency(b, grouping=True))


@mturk.command(help='Get historical costs from previous HITs')
@click.pass_obj
def costs(ctx):
    c = mturk_costs(ctx['session'])
    click.echo(locale.format_string('Number of videos: %i', c.count))
    click.echo('\nCosts per video\n' + '-' * 15)
    table = [
        ('Average:', locale.currency(c.average, grouping=True)),
        ('Median:', locale.currency(c.p50, grouping=True)),
        ('95th percentile:', locale.currency(c.p95, grouping=True)),
        ('Total:', locale.currency(c.total, grouping=True)),
    ]
    click.echo(tabulate(table, tablefmt='plain', colalign=('left', 'right')))


cli.add_command(mturk)
