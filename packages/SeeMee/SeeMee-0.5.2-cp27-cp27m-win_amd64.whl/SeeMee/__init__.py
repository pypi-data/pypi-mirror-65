import sys
from .base import main
from .info import __version__, __author__

def script_main():
    sys.exit(main(sys.argv))

__all__ = ['main', 'script_main']