"""Manage files with Micropython"""
import logging
from os.path import basename
import serial
import click

logger = logging.getLogger(__name__)


def send(ser, s):
    """Send message to serial device"""
    ser.write(b'%b\r' % s.encode())
    logger.debug(s)


def send_file(local_filename):
    """Send a file to Micropython"""
    with open(fn) as localfile:
        s = localfile.read()
    send(ctx['port'], \
        'with open({}, "wb") as remotefile: remotefile.write({})\n\r' \
        .format(repr(basename(local_filename)), repr(s)))


@click.group()
@click.option('-b', '--baud', metavar='<rate>', default=115200, \
        help='Port speed in baud.')
@click.option('-i', '--interrupt', is_flag=True, \
        help='Send soft interrupt (ctrl-c) before command.')
@click.option('-p', '--port', metavar='<port>', default='/dev/ttyUSB0', \
        help='Serial port device.')
@click.pass_context
def cli(ctx, baud, interrupt, port):
    """Manage files with Micropython"""
    port = serial.Serial(port, baud, timeout=1)
    if interrupt:
        send(port, '\x03')
    ctx.obj = {'port': port}


@cli.command()
@click.option('-r', '--reset', is_flag=True, \
        help='Send soft reset (ctrl-d) after copy.')
@click.argument('files', nargs=-1, required=True, type=click.File('rb'))
@click.pass_obj
def upload(ctx, reset, files):
    """Copy files to Micropython"""
    for f in files:
        send_file(f.name)
    if reset:
        send(ctx['port'], '\x04')
    ctx['port'].close()
