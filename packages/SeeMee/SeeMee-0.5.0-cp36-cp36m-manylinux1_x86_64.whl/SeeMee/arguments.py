import argparse
from .info import __version__

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('-V', '--version', action='version', version='SeeMee '+__version__)
argument_parser.add_argument('-s', '--size', '--output-size', type=int, dest='resolution', nargs=2, metavar=('WIDTH', 'HEIGHT'))
argument_parser.add_argument('-f', '--frame-rate', type=float, dest='framerate', metavar='FPS', default=0)
argument_parser.add_argument('-w', '--check-time', type=float, dest='check_time', metavar='SECONDS', default=1)
argument_parser.add_argument('-i', '--ignore-camera', dest='ignore_cameras', metavar='ID', type=int, action='append', default=[])
argument_parser.add_argument('-c', '--include-camera', dest='include_cameras', metavar='ID', type=int, action='append', default=[])

__all__ = ['argument_parser']