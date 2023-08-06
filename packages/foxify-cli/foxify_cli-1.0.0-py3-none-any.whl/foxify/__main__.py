from .config.startup import startup
from .core.argparser import ArgParser
import sys

def main():
    startup()
    parser = ArgParser(sys.argv[1:])
    parser.run_args()

if __name__ == "__main__":
    main()