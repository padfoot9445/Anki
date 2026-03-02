
from typing import Callable


def combinator_1(f):
    def curried(*x):
        return f(curried, *x)
    return curried
# so, we need some way to reference curried from inside itself without referencing the name.
# define a get_curried function:
f: Callable #parameter as above
def get_curried():
        def curried(*x):
            return f(get_curried(), *x)
        return curried
# but now we are referencing get_curried from inside itself
# so, use the old combinator
# we cannot directly use the old combinator on curried, because the API of curried is 
#      lambda *x: ...
# Therefore it is a public API that we are exporting to the function we call the new combinator on
# so we have to add an indirection via get_curried(self)
# all get_curried are called and never passed as a callback

def combinator(f):
    def get_curried(_get_curried): #_get_curried is the self param of get_curried, which is a function modified for use with the old combinator
        def curried(*x):
            return f(_get_curried(_get_curried), *x)
        return curried
    def old_combinator(g):
        return g(g)
    return old_combinator(get_curried)