"""Upload files to Micropython"""
import logging
from os.path import basename
import serial
import click

logger = logging.getLogger(__name__)


def send(ser, s):
    """Send message to serial device"""
    ser.write(b'%b\r' % s.encode())
    logger.debug(s)


@click.group()
@click.option('-b', '--baud', metavar='<rate>', default=115200, \
        help='Port speed in baud.')
@click.option('-d', '--delay', metavar='<delay>', default=100.0, \
        help='Delay between lines (ms).')
@click.option('-i', '--interrupt', is_flag=True, \
        help='Send soft interrupt (ctrl-c) before command.')
@click.option('-p', '--port', metavar='<port>', default='/dev/ttyUSB0', \
        help='Serial port device.')
@click.pass_context
def cli(ctx, baud, delay, interrupt, port):
    """Manage files with Micropython"""
    port = serial.Serial(port, baud, timeout=1)
    if interrupt:
        send(port, '\x03')
    ctx.obj = {'port': port, 'delay': delay}


@cli.command()
@click.option('-r', '--reset', is_flag=True, \
        help='Send soft reset (ctrl-d) after upload.')
@click.argument('files', nargs=-1, required=True, type=click.File('rb'))
@click.pass_obj
def upload(ctx, reset, files):
    """Upload files to Micropython"""
    for localfile in files:
        with open(localfile.name) as lf:
            s = lf.read()
        send(ctx['port'], \
            'with open({}, "wb") as remotefile: remotefile.write({})\n\r' \
            .format(repr(basename(localfile.name)), repr(s)))
    if reset:
        send(ctx['port'], '\x04')
    ctx['port'].close()
