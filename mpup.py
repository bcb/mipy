"""Upload file to Micropython"""
import serial
import time
import click

@click.command()
@click.option('--port', '-p', default='/dev/ttyUSB0', help='serial port device')
@click.option('--baud', '-b', default=115200, help='port speed in baud')
@click.option('--delay', '-d', default=100.0, help='delay between lines (ms)')
@click.option('--interrupt/--no-interrupt', '-i', help='send soft interrupt (ctrl-c) before upload')
@click.option('--reset/--no-reset', '-r', help='send soft reset (ctrl-d) after upload')
@click.argument('files', nargs=-1, type=click.File('rb'))
def cli():
    """Main cli entrypoint"""
    port = serial.Serial(args.port, args.baud)
    if args.interrupt:
        port.write(bytes('\x03', 'ascii'))
    for fh in args.files:
        port.write(bytes('_fh = open(%s, "w")\r' % repr(fh.name), 'ascii'))
        while True:
            s = fh.read(50)
            if len(s) == 0:
                break
            port.write(bytes('_fh.write(%s)\r' % repr(s), 'ascii'))
            time.sleep(args.delay/1000.0)
        port.write(bytes('_fh.close()\r', 'ascii'))
        fh.close()
    if args.reset:
        port.write(bytes('\x04', 'ascii'))
    port.close()
