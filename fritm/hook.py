#!/usr/bin/env python3

from pathlib import Path
import sys

import click
import frida

SCRIPT = (Path(__file__).parent / "script.js").read_text()


def spawn_and_hook(program, port=8080, filter="true", verbose="false"):
    pid = frida.spawn(program)
    hook(pid, port, filter, verbose)
    frida.resume(pid)


def hook(target, port=8080, filter="true", verbose="false"):
    session = frida.attach(target)
    script = SCRIPT.replace("PORT", str(port)).replace("FILTER", filter).replace("VERBOSE", verbose)
    frida_script = session.create_script(script)
    frida_script.load()


@click.command(help="Process: Unique name or PID of the process to attach to")
@click.argument("target")
@click.option(
    "-p",
    "--port",
    type=int,
    help="Local port to redirect to",
    default=8080,
    show_default=True,
)
@click.option(
    "--filter",
    type=str,
    help="filter expression",
    default="true",
    show_default=True,
)
@click.option(
    "--verbose",
    type=str,
    help="Log more info",
    default="false",
    show_default=True,
)
def _main_spawn(target, port, filter, verbose):
    spawn_and_hook(target, port, filter, verbose)
    if not sys.flags.interactive:
        sys.stdin.read()  # infinite loop


@click.command(help="Process: Unique name or PID of the process to attach to")
@click.argument("target")
@click.option(
    "-p",
    "--port",
    type=int,
    help="Local port to redirect to",
    default=8080,
    show_default=True,
)
@click.option(
    "--filter",
    type=str,
    help="filter expression",
    default="true",
    show_default=True,
)
@click.option(
    "--verbose",
    type=str,
    help="Log more info",
    default="false",
    show_default=True,
)
def _main_hook(target, port, filter, verbose):
    if str.isdigit(target):
        target = int(target)
    hook(target, port, filter, verbose)
    if not sys.flags.interactive:
        sys.stdin.read()  # infinite loop
