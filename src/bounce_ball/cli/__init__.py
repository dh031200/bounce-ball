# SPDX-FileCopyrightText: 2024-present dh031200 <imbird0312@gmail.com>
#
# SPDX-License-Identifier: MIT
import click

from bounce_ball.__about__ import __version__
from bounce_ball import BounceBall


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="bounce-ball")
def bounce_ball():
    game = BounceBall()
    game.show()
