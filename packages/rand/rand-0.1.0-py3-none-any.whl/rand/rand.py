import re
import sre_parse
import typing
from sre_parse import SubPattern
from sre_constants import LITERAL
from random import Random


class Rand:
    _random: Random

    def __init__(self, seed=None):
        self._random = Random()
        if seed:
            self.random_seed(seed)

    @property
    def random(self):
        return self._random

    def random_seed(self, seed=None):
        self._random.seed(seed)

    def register_parse(self, name: str, fn: typing.Callable[['Rand', typing.Any], typing.Any]):
        setattr(self, '_parse_%s' % name.lower(), fn)

    def _parse_subpattern(self, p):
        # input: (ro)
        # p: (SUBPATTERN, (1, 0, 0, [(LITERAL, 114), (LITERAL, 111)]))
        _, (_, _, _, pl) = p
        if len(pl) >= 2:
            if pl[0] == (LITERAL, 58) and pl[-1] == (LITERAL, 58):
                # input: (::)
                # p: (SUBPATTERN, (1, 0, 0, [(LITERAL, 58), (LITERAL, 58)]))
                # get the custom name
                token = self._parse_list(pl[1:-1])
                # get parser based on token with _parse_noop as default
                return getattr(self, '_parse_%s' % str(token).lower(), lambda ri, _: self._parse_noop(p))(self, p)
        return self._parse_list(p)

    def _parse_list(self, p):
        # p = [(LITERAL, 114), (LITERAL, 111)]
        return ''.join(filter(None, [self._parse(x) for x in p]))

    def _parse_branch(self, p):
        # input: ro|ko
        # p: [(BRANCH, (None, [[(LITERAL, 114), (LITERAL, 111)], [(LITERAL, 107), (LITERAL, 111)]]))]
        _, (_, vs) = p
        print(vs)
        return self._parse_noop(p)

    def _parse_in(self, p):
        # input: r|o
        # p: [(IN, [(LITERAL, 114), (LITERAL, 111)])]
        _, vs = p
        # get the list of sequence
        seq = [self._parse_list(v if isinstance(v, list) else [v]) for v in vs]
        return self.random.choice(seq)

    def _parse_literal(self, p):
        return chr(p[1])

    def _parse_noop(self, p):
        return ''

    def _parse(self, p) -> typing.Any:
        if isinstance(p, SubPattern):
            # handle subpattern class specially
            return self._parse_list(p)
        elif isinstance(p, tuple):
            token = p[0]
            # get parser based on token with _parse_noop as default
            return getattr(self, '_parse_%s' % str(token).lower(), self._parse_noop)(p)
        return ''

    def many(self, pattern: str, maps=None, filters=None, n: int = 1) -> typing.List[str]:
        # get normalised regex pattern from regex compiler
        regex_pattern: str = re.compile(pattern=pattern).pattern
        # return parsed pattern from regex
        # input: abc
        # output: [(LITERAL, 97), (LITERAL, 98), (LITERAL, 99)]
        regex_parsed: SubPattern = sre_parse.parse(regex_pattern)
        print(regex_parsed)
        # generate randomly X times
        rs = [self._parse(regex_parsed) for _ in range(n)]
        return rs

    def map(self, x):
        pass

    def _map_lower(self, opt=None):
        def _map_lower():
            pass

        pass

    def filter(self, x):
        pass


def en_name(ri: Rand, p: typing.Tuple[typing.Any]):
    return ri.random.choice(['test', 'test2', 'test3'])


rand = Rand(seed=28)
rand.register_parse('en_name', en_name)
print(rand.many('a|b|c|d|r|o|a', maps=[
    'lower',
    ('lower', []),
    ('replace', {'find': '', 'replace': ''})
], filters=[
    ('regex', {'pattern': ''})
], n=1))
