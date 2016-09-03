"""Manage files with Micropython"""
import logging
from os.path import basename
import serial
import click

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def _debug(message, *args, **kwargs):
    logger.debug(message, *args, **kwargs)


class Device(object):
    def __init__(self, port='/dev/ttyUSB0', baud='115200', interrupt=False,
            reset=False, timeout=1):
        self.port = port
        self.baud = baud
        self.interrupt = interrupt
        self.reset = reset
        self.timeout = timeout

    def __enter__(self):
        _debug('Opening {}'.format(self.port))
        self.serial = serial.Serial(self.port, self.baud, timeout=self.timeout)
        if self.interrupt:
            self.send_interrupt()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.reset:
            self.send_reset()
        _debug('Closing {}'.format(self.port))
        self.serial.close()

    def send(self, s):
        """Send message to serial device"""
        self.serial.write(b'%b\r' % s.encode())

    def send_file(self, local_filename):
        """Send a file to Micropython"""
        _debug('Sending {}'.format(local_filename))
        with open(local_filename) as localfile:
            s = localfile.read()
        self.send('with open({}, "wb") as remotefile: remotefile.write({})\n\r'\
            .format(repr(basename(local_filename)), repr(s)))

    def send_interrupt(self):
        """Send ctrl-c"""
        _debug('Interrupting')
        self.send('\x03')

    def send_reset(self):
        """Send ctrl-d"""
        _debug('Resetting')
        self.send('\x04')


@click.group()
@click.option('-b', '--baud', metavar='<rate>', default=115200, \
        help='Port speed in baud (default is 115200).')
@click.option('-i', '--interrupt', is_flag=True, \
        help='Send soft interrupt (ctrl-c) before command.')
@click.option('-p', '--port', metavar='<port>', default='/dev/ttyUSB0', \
        help='Serial port device (default is /dev/ttyUSB0).')
@click.option('-r', '--reset', is_flag=True, \
        help='Send soft reset (ctrl-d) after copy.')
@click.option('-t', '--timeout', default=1, \
        help='Timeout.')
@click.pass_context
def cli(ctx, *args, **kwargs):
    """Manage files with Micropython"""
    ctx.obj = {'args': args, 'kwargs': kwargs}


@cli.command()
@click.argument('files', nargs=-1, required=True, type=click.File('rb'))
@click.pass_obj
def cp(options, files):
    """Copy files to Micropython"""
    with Device(*options['args'], **options['kwargs']) as device:
        for f in files:
            device.send_file(f.name)
