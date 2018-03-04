"""
A script for simulating running a model training script.
"""

import sys
import time


if __name__ == '__main__':
    for i in range(10):
        time.sleep(1)
        print('time', i)

print('stderr', file=sys.stderr)
print('done')
