import itertools
import functools


__all__ = (  # noqa
    'b2kb', 'b2mb', 'b2gb', 'b2tb', 'b2pb', 'b2eb', 'b2zb', 'b2yb', 'kb2b', 'kb2mb',
    'kb2gb', 'kb2tb', 'kb2pb', 'kb2eb', 'kb2zb', 'kb2yb', 'mb2b', 'mb2kb', 'mb2gb',
    'mb2tb', 'mb2pb', 'mb2eb', 'mb2zb', 'mb2yb', 'gb2b', 'gb2kb', 'gb2mb', 'gb2tb',
    'gb2pb', 'gb2eb', 'gb2zb', 'gb2yb', 'tb2b', 'tb2kb', 'tb2mb', 'tb2gb', 'tb2pb',
    'tb2eb', 'tb2zb', 'tb2yb', 'pb2b', 'pb2kb', 'pb2mb', 'pb2gb', 'pb2tb', 'pb2eb',
    'pb2zb', 'pb2yb', 'eb2b', 'eb2kb', 'eb2mb', 'eb2gb', 'eb2tb', 'eb2pb', 'eb2zb',
    'eb2yb', 'zb2b', 'zb2kb', 'zb2mb', 'zb2gb', 'zb2tb', 'zb2pb', 'zb2eb', 'zb2yb',
    'yb2b', 'yb2kb', 'yb2mb', 'yb2gb', 'yb2tb', 'yb2pb', 'yb2eb', 'yb2zb', 'b2any')
SYMBOLS = ('b', 'kb', 'mb', 'gb', 'tb', 'pb', 'eb', 'zb', 'yb')
NAMES = ('byte', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte',
         'petabyte', 'exabyte', 'zettabyte', 'yottabyte')
SIZES = tuple(1024**i for i in range(0, len(SYMBOLS)))
REVERSED = tuple(reversed(tuple(zip(SYMBOLS, NAMES, enumerate(SIZES)))))


def _2_(value, roundto=2, *, _=None):
    b = SYMBOLS.index(_[1])
    x = SIZES[SYMBOLS.index(_[0])]
    y = SIZES[b]
    # if `something 2 bytes` then rounded is doesn't not need to be true.
    if not b:
        roundto = 0
    k = value*x
    if 0 in (x, y):
        r = k if (x > y) else round(k/y, roundto)
    else:
        r = round(k/y, roundto)
    return int(r) if r.is_integer() else r


# assign name to callback function
for _ in itertools.permutations(SYMBOLS, 2):
    '''
        >>> b2kb(1024)
        1
    '''
    locals()[f'{_[0]}2{_[1]}'] = functools.partial(_2_, _=_)


class b2any(str):

    __slots__ = ('size', 'name', 'symbol')
    __module__ = str.__module__

    def __new__(cls, value, sep=' ', rounded=2):
        ''' Bytes to any type like kilobyte, megabyte, ...

            Type
                value:    int
                sep:      str
                rounded:  int
                return:   str

            Example
                >>> a = b2any(2560)
                >>> a
                '2.5 KB'
                >>> a.name
                'kilobyte'
                >>> a.size
                2.5
                >>> a.symbol
                'KB'

                >>> b = b2any(100)
                >>> b
                '100 bytes'
                >>> b.name
                'bytes'
                >>> b.size
                100
                >>> b.symbol
                'B'

                >>> c = b2any(1)
                >>> c
                '1 byte'
                >>> c.name
                'byte'
                >>> c.size
                1
                >>> c.symbol
                'B'
        '''
        if value < 0:
            _ = f'`{cls.__class__.__name__}(value)` can not be `< 0`'
            raise ValueError(_)

        # process
        for symbol, name, (index, size) in REVERSED:
            if value >= size:
                break

        # size
        s = round(value/size if value or size else 0, rounded)
        cls.size = int(s) if s.is_integer() else s
        # e.g. `byte`, `bytes`, `kilobyte`, ...
        cls.name = f'{name}s' if not index and cls.size > 1 else name
        cls.symbol = symbol.upper()
        return str.__new__(cls, f'{cls.size}{sep}{cls.symbol if index else cls.name}')
