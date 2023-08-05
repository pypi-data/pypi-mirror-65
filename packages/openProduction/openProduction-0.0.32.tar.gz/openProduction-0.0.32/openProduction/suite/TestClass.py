from openProduction.common import Exceptions
import threading

class TestClass:
    def __init__(self):
        self._abort_event = threading.Event()
        self._unload_event = threading.Event()
        
    def abort(self):
        self._abort_event.set()
        
    def abortClear(self):
        self._abort_event.clear()
        
    def unload(self):
        self._unload_event.set()
        
    def unloadClear(self):
        self._unload_event.clear()
    
    def installRunner(self, runner):
        return True
    
    def install(self, suite):
        return True
    
    def _preAssert(self):
        if self._abort_event.is_set():
            raise Exceptions.OpenProductionAbortError("")
            
    def evalAssert(self, okay, msg, ignoreAbort):
        if not ignoreAbort:
            self._preAssert()
        if not okay:
            raise Exceptions.OpenProductionAssertionError(msg)
    
    def assertEqual(self, val, comp, msg=None, ignoreAbort=False):
        if msg == None:
            msg="Assertion error %s!=%s"%(str(val), str(comp))
        self.evalAssert(val == comp, msg, ignoreAbort)

    def assertGreaterEqual(self, val, comp, msg=None, ignoreAbort=False):
        if msg == None:
            msg="Assertion error %s<%s"%(str(val), str(comp))
        self.evalAssert(val >= comp, msg, ignoreAbort)

    def assertGreater(self, val, comp, msg=None, ignoreAbort=False):
        if msg == None:
            msg="Assertion error %s<=%s"%(str(val), str(comp))
        self.evalAssert(val > comp, msg, ignoreAbort)

    def assertLessEqual(self, val, comp, msg=None, ignoreAbort=False):
        if msg == None:
            msg="Assertion error %s>%s"%(str(val), str(comp))
        self.evalAssert(val <= comp, msg, ignoreAbort)

    def assertLess(self, val, comp, msg=None, ignoreAbort=False):
        if msg == None:
            msg="Assertion error %s>=%s"%(str(val), str(comp))
        self.evalAssert(val < comp, msg, ignoreAbort)

    def assertInRange(self, val, minRange, maxRange, msg=None, ignoreAbort=False):
        if msg == None:
            msg="Assertion error %s!=[%s...%s]"%(str(val), str(minRange), str(maxRange))
        self.evalAssert(val >= minRange and val <= maxRange, msg, ignoreAbort)
        
    def assertNotEqual(self, val, comp, msg=None, ignoreAbort=False):
        if msg == None:
            msg="Assertion error %s==%s"%(str(val), str(comp))
        self.evalAssert(val != comp, msg, ignoreAbort)