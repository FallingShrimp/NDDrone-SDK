import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from analyzer import behaviour as NeuroApiInterpreter
from analyzer.runner import NeuroApiRunner


def main():
    NeuroApiInterpreter.init()
    neuroApi = NeuroApiRunner()
    neuroApi.start()


if __name__ == "__main__":
    main()
