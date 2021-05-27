import sys

from config.path import project

sys.path.insert(0, str(project))

if __name__ == '__main__':
    from pytrieval import Pytrieval
    Pytrieval().run()
