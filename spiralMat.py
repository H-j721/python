import itertools
# -*- coding:utf-8 -*-

"""
Print Spiral Matrix
"""

# Create time   : 2016-04-03 21:21
# Last modified : 2016-04-03 21:52
#########################################################


def spiral(n, m):
    _status = itertools.cycle(['right', 'down', 'left', 'up'])
    _movemap = {
        'right': (1, 0), 
        'down': (0, 1),
        'left': (-1, 0),
        'up': (0, -1),
    }
    pos2no = dict.fromkeys([(x, y) for x in range(n) for y in range(m)])
    _pos = (0, 0)
    _st = next(_status)

    for i in range(1, n * m + 1):
        _oldpos = _pos
        _pos = tuple(map(sum, zip(_pos, _movemap[_st])))
        if (_pos not in pos2no) or (pos2no[_pos]):
            _st = next(_status)
            _pos = tuple(map(sum, zip(_oldpos, _movemap[_st])))
        pos2no[_oldpos] = i
    return pos2no


def display_spiral(n, m):
    pos2no = spiral(n, m)
    for i in range(m):
        for j in range(n):
            print pos2no[(j, i)], '\t',
        print '\n'
    print '-' * 30


if __name__ == '__main__':
    display_spiral(3, 3)
    display_spiral(6, 6)
    display_spiral(4, 5)
    display_spiral(4, 10)
