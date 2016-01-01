from __future__ import with_statement
from __future__ import absolute_import

import abc
import functools
import sys
import unittest

from backports.functools_partialmethod import partialmethod


def capture(*args, **kw):
    """capture all positional and keyword arguments"""
    return args, kw


class TestPartialMethod(unittest.TestCase):

    class A(object):
        nothing = partialmethod(capture)
        positional = partialmethod(capture, 1)
        keywords = partialmethod(capture, a=2)
        both = partialmethod(capture, 3, b=4)

        nested = partialmethod(positional, 5)

        over_partial = partialmethod(functools.partial(capture, c=6), 7)

        static = partialmethod(staticmethod(capture), 8)
        cls = partialmethod(classmethod(capture), d=9)

    a = A()

    def test_arg_combinations(self):
        self.assertEqual(self.a.nothing(), ((self.a,), {}))
        self.assertEqual(self.a.nothing(5), ((self.a, 5), {}))
        self.assertEqual(self.a.nothing(c=6), ((self.a,), {'c': 6}))
        self.assertEqual(self.a.nothing(5, c=6), ((self.a, 5), {'c': 6}))

        self.assertEqual(self.a.positional(), ((self.a, 1), {}))
        self.assertEqual(self.a.positional(5), ((self.a, 1, 5), {}))
        self.assertEqual(self.a.positional(c=6), ((self.a, 1), {'c': 6}))
        self.assertEqual(self.a.positional(5, c=6), ((self.a, 1, 5), {'c': 6}))

        self.assertEqual(self.a.keywords(), ((self.a,), {'a': 2}))
        self.assertEqual(self.a.keywords(5), ((self.a, 5), {'a': 2}))
        self.assertEqual(self.a.keywords(c=6), ((self.a,), {'a': 2, 'c': 6}))
        self.assertEqual(self.a.keywords(5, c=6), ((self.a, 5), {'a': 2, 'c': 6}))

        self.assertEqual(self.a.both(), ((self.a, 3), {'b': 4}))
        self.assertEqual(self.a.both(5), ((self.a, 3, 5), {'b': 4}))
        self.assertEqual(self.a.both(c=6), ((self.a, 3), {'b': 4, 'c': 6}))
        self.assertEqual(self.a.both(5, c=6), ((self.a, 3, 5), {'b': 4, 'c': 6}))

        self.assertEqual(self.A.both(self.a, 5, c=6), ((self.a, 3, 5), {'b': 4, 'c': 6}))

    def test_nested(self):
        self.assertEqual(self.a.nested(), ((self.a, 1, 5), {}))
        self.assertEqual(self.a.nested(6), ((self.a, 1, 5, 6), {}))
        self.assertEqual(self.a.nested(d=7), ((self.a, 1, 5), {'d': 7}))
        self.assertEqual(self.a.nested(6, d=7), ((self.a, 1, 5, 6), {'d': 7}))

        self.assertEqual(self.A.nested(self.a, 6, d=7), ((self.a, 1, 5, 6), {'d': 7}))

    def test_over_partial(self):
        self.assertEqual(self.a.over_partial(), ((self.a, 7), {'c': 6}))
        self.assertEqual(self.a.over_partial(5), ((self.a, 7, 5), {'c': 6}))
        self.assertEqual(self.a.over_partial(d=8), ((self.a, 7), {'c': 6, 'd': 8}))
        self.assertEqual(self.a.over_partial(5, d=8), ((self.a, 7, 5), {'c': 6, 'd': 8}))

        self.assertEqual(self.A.over_partial(self.a, 5, d=8), ((self.a, 7, 5), {'c': 6, 'd': 8}))

    def test_bound_method_introspection(self):
        obj = self.a
        self.assertIs(obj.both.__self__, obj)
        self.assertIs(obj.nested.__self__, obj)
        self.assertIs(obj.over_partial.__self__, obj)
        self.assertIs(obj.cls.__self__, self.A)
        self.assertIs(self.A.cls.__self__, self.A)

    def test_unbound_method_retrieval(self):
        obj = self.A
        if sys.version_info.major >= 3:
          self.assertFalse(hasattr(obj.both, "__self__"))
          self.assertFalse(hasattr(obj.nested, "__self__"))
          self.assertFalse(hasattr(obj.over_partial, "__self__"))
        else:
          self.assertIsNone(obj.both.__self__)
          self.assertIsNone(obj.nested.__self__)
          self.assertIsNone(obj.over_partial.__self__)
        self.assertFalse(hasattr(obj.static, "__self__"))
        self.assertFalse(hasattr(self.a.static, "__self__"))

    def test_descriptors(self):
        for obj in [self.A, self.a]:
            self.assertEqual(obj.static(), ((8,), {}))
            self.assertEqual(obj.static(5), ((8, 5), {}))
            self.assertEqual(obj.static(d=8), ((8,), {'d': 8}))
            self.assertEqual(obj.static(5, d=8), ((8, 5), {'d': 8}))

            self.assertEqual(obj.cls(), ((self.A,), {'d': 9}))
            self.assertEqual(obj.cls(5), ((self.A, 5), {'d': 9}))
            self.assertEqual(obj.cls(c=8), ((self.A,), {'c': 8, 'd': 9}))
            self.assertEqual(obj.cls(5, c=8), ((self.A, 5), {'c': 8, 'd': 9}))

    def test_overriding_keywords(self):
        self.assertEqual(self.a.keywords(a=3), ((self.a,), {'a': 3}))
        self.assertEqual(self.A.keywords(self.a, a=3), ((self.a,), {'a': 3}))

    def test_invalid_args(self):
        with self.assertRaises(TypeError):
            class B(object):
                method = partialmethod(None, 1)

    def test_repr(self):
        self.assertEqual(repr(vars(self.A)['both']),
                         'backports.functools_partialmethod.partialmethod({}, 3, b=4)'.format(capture))

    def test_abstract(self):
        class Abstract(abc.ABCMeta):

            @abc.abstractmethod
            def add(self, x, y):
                pass

            add5 = partialmethod(add, 5)

        self.assertTrue(Abstract.add.__isabstractmethod__)
        self.assertTrue(Abstract.add5.__isabstractmethod__)

        for func in [self.A.static, self.A.cls, self.A.over_partial, self.A.nested, self.A.both]:
            self.assertFalse(getattr(func, '__isabstractmethod__', False))

if __name__ == '__main__':
    unittest.main()
