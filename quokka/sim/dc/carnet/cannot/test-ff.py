from quokka.sim.event import *
import unittest

class TestEvent(unittest.TestCase):
    def testFF(self):
        event = Event()
        mdp = event.runFF()

if __name__ == '__main__':
    unittest.main()
