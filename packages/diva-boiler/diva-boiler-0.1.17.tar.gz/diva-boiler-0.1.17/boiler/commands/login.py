import os
import webbrowser

import click
import requests
from xdg import BaseDirectory

from boiler import BOILER_CONFIG_PATH, BOILER_CREDENTIAL_FILE, cli


def _is_valid_stumpf_token(stumpf_url, token):
    # note - don't use the boiler session since that could have an old token,
    # and automatically fails on auth failures.
    return requests.get(stumpf_url + '/api/v1/user/me', headers={'X-Stumpf-Token': token}).ok


@cli.command(name='login')
@click.pass_obj
def login(ctx):
    click.echo('A browser window has been opened, login and copy the token to login.', err=True)
    webbrowser.open(ctx['stumpf_url'] + '/login?next=/token')

    while True:
        stumpf_token = click.prompt('Token', err=True)
        if _is_valid_stumpf_token(ctx['stumpf_url'], stumpf_token):
            with open(
                os.path.join(
                    BaseDirectory.load_first_config(BOILER_CONFIG_PATH), BOILER_CREDENTIAL_FILE
                ),
                'w',
            ) as outfile:
                outfile.write(stumpf_token)
            return click.echo(click.style('You are now logged in.', fg='green'), err=True)
        else:
            click.echo(
                click.style(
                    "Your token doesn't appear to be valid, did you copy/paste correctly?",
                    fg='yellow',
                ),
                err=True,
            )
