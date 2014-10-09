from quokka.util.defines import *
from quokka.util.ds import *
from unittest import TestCase
import unittest

class Test(TestCase):

    def test2dMap(self):
        twodmap = TwoDMap()
        self.assertFalse(twodmap.has_key(1,2))
        twodmap[1][2] = 3
        self.assertTrue(twodmap.has_key(1,2))
        self.assertTrue(twodmap[1][2] == 3)
        del twodmap[1][2]
        self.assertFalse(twodmap.has_key(1,2))

if __name__ == '__main__':
    unittest.main()

