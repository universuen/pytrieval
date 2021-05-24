import sys
import os

sys.path.insert(0, os.getcwd())

if __name__ == '__main__':
    from pytrieval import Pytrieval
    Pytrieval().run()
