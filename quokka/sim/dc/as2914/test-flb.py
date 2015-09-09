from quokka.sim.event import *
import unittest

class TestEvent(unittest.TestCase):
    def testFLB(self):    
        event = Event()
        mdp = event.runFLB()
    """
    def testQuokka(self):
        event = Event()
        pla, mdp = event.run()
    """
    """
    def testFF(self):
        event = Event()
        mdp = event.runFF()
    """

if __name__ == '__main__':
    unittest.main()
