import logging
from openProduction.common import misc, Signals, Exceptions
from openProduction.suite import TestSuiteIO, TestClass, TestParams
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
import time
import traceback


class InstallHints:
    def __init__(self, shouldBeLast=False, mustBeLast=False):
        self.mustBeLast = mustBeLast
        self.shouldBeLast = shouldBeLast

class StepType(Enum):
    SETUP = 0
    REGULAR = 1
    TEARDOWN = 2
    LOAD = 3
    UNLOAD = 4
    
class SuiteState(Enum):
    LOADING = 0
    REGULAR = 1
    UNLOADING = 2

class ExecutionResult(Enum):
    SUCCESS = 0
    FAIL = 1
    EXCEPTION = 2
    ABORT = 3
    SKIP = 4
    NOTEXECUTED = 5

class StepResult:
    def __init__(self, result, case, msg, duration):
        self.result = result
        self.case = case
        self.msg = msg
        self.duration = duration
            
    def __str__(self):
        return "result=%s, name=%s, msg=%s, duration=%.02f"%(self.result, self.case.getFullName(), self.msg, self.duration)
    
    def toDict(self):
        return {"result": self.result.value, "msg": self.msg, "duration": self.duration, "tc": self.case.toDict()}


class TestSuiteLogger(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self.txt = ""

    def emit(self, record):
        if self.txt != "":
            self.txt += "\n"
        self.txt += self.format(record)

class SuiteResult:
    def __init__(self, suite):
        self.numTotal = 0
        self.numErrors = 0
        self.numFails = 0
        self.numSkips = 0
        self.numAbort = 0
        self.numGood = 0
        self.stepResults = []
        self.executionTime = 0
        self.suite = suite
        
        logger = logging.getLogger(misc.getAppName())
        self.testSuiteLogger = TestSuiteLogger()
        self.testSuiteLogger.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(self.testSuiteLogger)

    def addStepResult(self, stepResult):
        self.numTotal += 1
        self.stepResults.append(stepResult)
        if stepResult.result == ExecutionResult.EXCEPTION:
            self.numErrors +=1
        elif stepResult.result == ExecutionResult.FAIL:
            self.numFails += 1
        elif stepResult.result == ExecutionResult.SKIP:
            self.numSkips += 1
        elif stepResult.result == ExecutionResult.SUCCESS:
            self.numGood += 1
        elif stepResult.result == ExecutionResult.ABORT:
            self.numAbort += 1
            
    def finalize(self, executionTime):
        self.executionTime = executionTime
        logger = logging.getLogger(misc.getAppName())
        logger.removeHandler(self.testSuiteLogger)
    
    def isSuccessful(self):
        if self.numErrors != 0 or self.numFails != 0 or self.numAbort != 0:
            return False
        else:
            return True
        
    def toDict(self):
        rv = {"numTotal": self.numTotal, "numErrors": self.numErrors, "numFails": self.numFails, 
              "numSkips": self.numSkips, "numGood": self.numGood, "numAbort": self.numAbort,
              "executionTime": self.executionTime, "stepResults": []}
        for res in self.stepResults:
            rv["stepResults"].append(res.toDict())
        return rv
    
    def getLogText(self):
        return self.testSuiteLogger.txt
    
    def __str__(self):
        rv = self._reportErrors()
        rv += self._reportOverall()
        
        attrs = self.suite.values
        if len(attrs) > 0:
            rv += "\n----------------------------------------------------------------------\n"
            rv += "The test suite contains the following values:\n"
            rv += str(attrs) + "\n"
            rv += "----------------------------------------------------------------------\n"
        return rv
        
    def _reportErrors(self):
        rv = ""
        for res in self.stepResults:
            if res.result == ExecutionResult.EXCEPTION:
                failStr = "ERROR"
            elif res.result == ExecutionResult.FAIL:
                failStr = "FAIL"
            elif res.result == ExecutionResult.ABORT:
                failStr = "ABORT"
            else:
                continue
            rv += "======================================================================\n"
            rv += "%s: %s (%s)\n%s\n"%(failStr, res.case.name, res.case.group.name, res.case.doc)
            rv += "----------------------------------------------------------------------\n"
            rv += res.msg + "\n"
        return rv
        
    def _reportOverall(self):
        rv = "----------------------------------------------------------------------\n"
        dur = self.executionTime
        numTests = self.numTotal
        numGood = self.numGood
        numFail = self.numFails
        numAbort = self.numAbort
        numError = self.numErrors
        numSkip = self.numSkips
        rv += "Ran %d step(s) in %.03f s\n\n"%(numTests, dur)
        if self.isSuccessful() == False:
            overall = "FAILED (failures=%d, errors=%d, abort=%d, skip=%d, ok=%d)"%(numFail,
                              numError, numAbort, numSkip, numGood)
        else:
            overall = "OK (failures=%d, errors=%d, abort=%d, skip=%d, ok=%d)"%(numFail,
                              numError, numAbort, numSkip, numGood)
        rv += overall+"\n"
        return rv

class TestCase:
    def __init__(self, name, doc, func, typ, installHint):
        self.name = name
        self.doc = doc
        self.func = func
        self.typ = typ
        self.group = None
        self.installHint = installHint
        
    def getFullName(self):
        name = ""
        if self.group != None:
            name += self.group.name + "."
        name += self.name
        return name
    
    def toDict(self):
        rv =  {"name": self.name, "doc": self.doc, "typ": self.typ.value}
        if self.group != None:
            rv["group"] = {"name":self.group.name, "doc":self.group.doc}
        return rv


class TestCaseSort:
    @staticmethod
    def sortByHints(testCases):
        logger = logging.getLogger(misc.getAppName())
        idx=0
        for tc in testCases:
            if tc.installHint.shouldBeLast == True:
                #push element to end
                testCases.insert(len(testCases), testCases.pop(idx))
            idx+=1
            
        idx=0
        numLast=0
        for tc in testCases:
            if tc.installHint.mustBeLast == True:
                #push element to end
                testCases.insert(len(testCases), testCases.pop(idx))
                numLast+=1
            idx+=1
            
        if numLast > 1:
            logger.warning("more than one test case marked as 'mustBeLast', ordering may be unexpected")
        
        return testCases

class TestCaseGroup:
    def __init__(self, name, doc, testClass):
        self.logger = logging.getLogger(misc.getAppName())
        if isinstance(testClass, TestClass.TestClass) == False:
            raise RuntimeError ("testClass must be of type openProduction.suite.TestClass.TestClass")
        
        self.testClass = testClass
        self.name = name
        self.doc = doc
        self._tcs = []
        self.runnerInstalled = False
    
    def install(self, suite):
        return self.testClass.install(suite)
    
    def addTestCase(self, tc, index=None):
        tc.group = self
        if index == None:
            index=len(self._tcs)
        self._tcs.insert(index, tc)
        
    def getFullName(self):
        return self.name
    
    def getNumTCs(self):
        return len(self._tcs)
    
    def getTCs(self, typ, sort=True):
        myTcl = []
        for t in self._tcs:
            if t.typ == typ:
                myTcl.append(t)
                
        if sort:
            def myFunc(obj):
                return obj.getFullName()
            myTcl.sort(key=myFunc)
            
        myTcl = TestCaseSort.sortByHints(myTcl)
                
        return myTcl

    def getTestCases(self, sort=True):
        return self.getTCs(StepType.REGULAR, sort)
        
    def getSetUps(self, sort=True):
        return self.getTCs(StepType.SETUP, sort)
                
    def getTearDowns(self, sort=True):
        return self.getTCs(StepType.TEARDOWN, sort)
    
    def getLoaders(self, sort=True):
        return self.getTCs(StepType.LOAD, sort)
    
    def getUnLoaders(self, sort=True):
        return self.getTCs(StepType.UNLOAD, sort)

class TestSuite:
    def __init__(self, name, doc, params=None, values=None, tempParams=None):
        self.logger = logging.getLogger(misc.getAppName())
        self.name = name
        self.doc = doc
                    
        self.runner = None
        
        if params != None:
            if isinstance(params, TestParams.TestParams) == False:
                raise RuntimeError("params has to be of type TestParams.TestParams")
        if values != None:
            if isinstance(values, TestParams.TestParams) == False:
                raise RuntimeError("values has to be of type TestParams.TestParams")
        if tempParams != None:
            if isinstance(tempParams, TestParams.TestParams) == False:
                raise RuntimeError("tempParams has to be of type TestParams.TestParams")

            
        self.params = params
        if values == None:
            self.values = TestParams.TestParams({}, None)
        else:
            self.values = values
        if tempParams == None:
            self.tempParams = TestParams.TestParams({}, None)
        else:
            self.tempParams = tempParams
        self._tcg = []
        
    def _validate(self):
        tcLastName = ""
        funcs = [self.getTestCases, self.getSetUps, self.getTearDowns, 
                 self.getLoaders, self.getUnLoaders]
        
        for func in funcs:
            anyML = False
            tcg = func()
            for tc in tcg:
                if tc.installHint.mustBeLast == True:
                    if anyML == True:
                        raise RuntimeError("both testcases %s and %s have installation hint 'mustBeLast'"%(tcLastName, tc.name))
                    anyML = True
                    tcLastName = tc.name
                    
        return True
    
    def abort(self):
        for tg in self._tcg:
            tg.testClass.abort()

    def abortClear(self):
        for tg in self._tcg:
            tg.testClass.abortClear()

    def unload(self):
        for tg in self._tcg:
            tg.testClass.unload()

    def unloadClear(self):
        for tg in self._tcg:
            tg.testClass.unloadClear()
        
    def installRunner(self, runner):
        self.runner = runner
        for tcg in self._tcg:
            if tcg.testClass.runnerInstalled == False:
                rv = tcg.testClass.installRunner(runner)
                if rv == False:
                    raise RuntimeError("intallation of runner@group %s failed"%tcg.name)
                tcg.testClass.runnerInstalled = True
        
    def addMethodHint(self, func, installHint):
        tc = self.getTCBYFunc(func)
        if tc != None:
            tc.installHint = installHint
            
        self._validate()
    
    def addTestCaseGroup(self, tcg, index=None):
        rv = None
        if isinstance(tcg, TestCaseGroup):
            self._tcg.append(tcg)
            rv = tcg.install(self)
            if rv != False:
                self._validate()
                if self.runner != None:
                    rv = tcg.testClass.installRunner(self.runner)
                    if rv == False:
                        raise RuntimeError("intallation of runner@group %s failed"%tcg.name)
                    tcg.testClass.runnerInstalled = True
        else:
            raise RuntimeError("param tcg has to be a TestCaseGroup")
        return rv
        
    def getTCBYFunc(self, func):
        rv = None
        for tg in self._tcg:
            for tc in tg._tcs:
                if tc.func == func:
                    rv = tc
                    break
        return rv
    
    def getNumTCs(self):
        numCases = 0
        for tg in self._tcg:
            numCases += tg.getNumTCs()    
        return numCases
        
    def getTCs(self, typ, sort=True):
        myTcl = []
        for tg in self._tcg:
            tcs = tg.getTCs(typ, sort)
            for tc in tcs:
                myTcl.append(tc)
                
        if sort:
            def myFunc(obj):
                return obj.getFullName()
            myTcl.sort(key=myFunc)
            
        myTcl = TestCaseSort.sortByHints(myTcl)
            
        return myTcl

    def getTestCases(self, sort=True):
        return self.getTCs(StepType.REGULAR, sort)
        
    def getSetUps(self, sort=True):
        return self.getTCs(StepType.SETUP, sort)
                
    def getTearDowns(self, sort=True):
        return self.getTCs(StepType.TEARDOWN, sort)
    
    def getLoaders(self, sort=True):
        return self.getTCs(StepType.LOAD, sort)
    
    def getUnLoaders(self, sort=True):
        return self.getTCs(StepType.UNLOAD, sort)
    
    def getTestCaseGroups(self):
        return self._tcg
    
class TestSuiteRunner:
    
    def __init__(self, testSuite, stopOnFail=True, stopOnExcept=True, stopOnAbort=True):
        self.logger = logging.getLogger(misc.getAppName())
        
        self.testSuite = testSuite
        
        self.sequenceStart = Signals.Signal()
        self.sequenceComplete = Signals.Signal()
        self.stepStart = Signals.Signal()
        self.stepComplete = Signals.Signal()
        self.signalError = Signals.Signal()
        self.prepareNextRun = Signals.Signal()
        self.keyChanged = Signals.Signal()
        self.deviceIDSet = Signals.Signal()
        
        testSuite.values.keyChanged.connect(self.keyChanged)
        testSuite.values.deviceIDSet.connect(self.deviceIDSet)
        
        self._stopOnFail = stopOnFail
        self._stopOnExcept = stopOnExcept
        self._stopOnAbort = stopOnAbort
        self.isExecuting = False
        self.isLoaded = False
        
        self._pool = ThreadPoolExecutor(3)
        
        self.testSuite.installRunner(self)
        
        if self.testSuite.params != None:
            self.testSuite.params.setReadOnly(True)
        
        self.suiteResults = None
        self._abortRun = False
            
    def _executeCases(self, executionType, cases, stopOnExcept=True, stopOnFail=True, stopOnAbort=True):
        rv = True
        
        curIdx = 0
        for case in cases:
            self.stepStart.emit(executionType, case, curIdx, len(cases))
            stepStart = time.time()
                
            try:
                res = ExecutionResult.SUCCESS
                msg = "Ok"
                rv = case.func(self.testSuite.params, self.testSuite.values)
                if rv != None:
                    if rv == ExecutionResult.SKIP:
                        res = ExecutionResult.SKIP
                        msg = "Skip"
                    elif isinstance(rv, TestCaseGroup):
                        self.testSuite.addTestCaseGroup(rv)
                        self.logger.info("test case group %s added to test suite"%rv.getFullName())
                    elif isinstance(rv, TestSuiteIO.IOMessage):
                        msg = rv.msg
                    elif type(rv) == type([]):
                        for val in rv:
                            if isinstance(val, TestCaseGroup):
                                self.testSuite.addTestCaseGroup(val)
                                self.logger.info("test case group %s added to test suite"%val.getFullName())
                    else:
                        pass
                rv = True
                if case.installHint.mustBeLast == True and curIdx+1 != len(cases):
                    msg = "case.mustBeLast set, but idx=%d of %d"%(curIdx+1, len(cases))
                    res = ExecutionResult.FAIL
                    rv = False
                
            except Exceptions.OpenProductionAssertionError:
                msg = traceback.format_exc()
                res = ExecutionResult.FAIL
                rv = False
            except Exceptions.OpenProductionAbortError:
                msg = traceback.format_exc()
                res = ExecutionResult.ABORT
                rv = False
            except:
                msg = traceback.format_exc()
                res = ExecutionResult.EXCEPTION
                rv = False
                
            if (res == ExecutionResult.SUCCESS or res == ExecutionResult.SKIP) and self._abortRun == True:
                res = ExecutionResult.ABORT
                msg = "Abort"
                
            stepEnd = time.time()
            duration = stepEnd - stepStart
            
            result = StepResult(res, case, msg, duration)
            self.suiteResults.addStepResult(result)
                
            self.stepComplete.emit(executionType, result, curIdx, len(cases))
            
            curIdx+=1
            
            if res == ExecutionResult.EXCEPTION and stopOnExcept:
                break
            elif res == ExecutionResult.FAIL and stopOnFail:
                break
            elif res == ExecutionResult.ABORT and stopOnAbort:
                break
            
        return rv
        
    def _executeSuite(self, executionType):      
        executionStart = time.time()
        self.suiteResults = SuiteResult(self.testSuite)
        self.testSuite.values.clear()
        
        skipTearDown = False
        self.sequenceStart.emit(executionType)
        
        resultsFinalized = False
        
        if executionType == SuiteState.REGULAR:
            cases = self.testSuite.getSetUps()
            self._executeCases(executionType, cases, stopOnExcept=True, stopOnFail=True, stopOnAbort=True)
            
            if self.suiteResults.isSuccessful():
                cases = self.testSuite.getTestCases()
                self._executeCases(executionType, cases, self._stopOnExcept, self._stopOnFail, self._stopOnAbort)
            else:
                skipTearDown = True
                
            resultsFinalized = True
            executionEnd = time.time()
            duration = executionEnd - executionStart
            self.suiteResults.finalize(duration)
                        
            if skipTearDown == False:
                cases = self.testSuite.getTearDowns()
                self._executeCases(executionType, cases, stopOnExcept=False, stopOnFail=False, stopOnAbort=False)
        elif executionType == SuiteState.LOADING:
            cases = self.testSuite.getLoaders()
            self._executeCases(executionType, cases, stopOnExcept=True, stopOnFail=True, stopOnAbort=True)
        elif executionType == SuiteState.UNLOADING:
            cases = self.testSuite.getUnLoaders()
            self._executeCases(executionType, cases, stopOnExcept=False, stopOnFail=False, stopOnAbort=False)
        
        
        if resultsFinalized == False:
            executionEnd = time.time()
            duration = executionEnd - executionStart
            self.suiteResults.finalize(duration)
                
        if executionType == SuiteState.LOADING and self.suiteResults.isSuccessful():
            self.isLoaded = True
        elif executionType == SuiteState.UNLOADING:
            self.isLoaded = False

        self.testSuite.abortClear()
        self._abortRun = False
        self.isExecuting = False

        try:
            self.sequenceComplete.emit(executionType, self.suiteResults, self.testSuite.params, self.testSuite.values)
        except:
            self.logger.error("full traceback:\n%s"%(traceback.format_exc()))

        if (executionType == SuiteState.REGULAR):
            try:
                self.prepareNextRun.emit(self.suiteResults)
            except:
                self.logger.error("full traceback:\n%s"%(traceback.format_exc()))


        self.testSuite.values.clear()

        return self.suiteResults
    
    def abort(self):
        self.logger.info("TestSuiteRunner abort requested")
        self._abortRun = True
        self.testSuite.abort()
    
    def loadSuite(self):
        return self._execute(SuiteState.LOADING, msg="Can't load suite, the product is still running")
        
    def unloadSuite(self):
        return self._execute(SuiteState.UNLOADING, msg="Can't unload suite, the product is still running")

    def run(self):
        if self.isLoaded == False:
            self.logger.warning("Can't run an unloaded test suite")
            return None
        return self._execute(SuiteState.REGULAR)
        
    def _execute(self, executionType, msg="Can't start product run, the product is still running"):
        #run test suite methods asynchronously
        if self.isExecuting == True:
            self.logger.warning(msg)
            return None
        
        if executionType == SuiteState.LOADING:
            self._abortRun = False
            self.testSuite.abortClear()
            self.testSuite.unloadClear()
        elif executionType == SuiteState.UNLOADING:
            self.testSuite.unload()
        
        self.isExecuting = True
        future = self._pool.submit(self._executeSuite, (executionType))
        future.add_done_callback(self._onExecutionDone)
        return future

    def _onExecutionDone(self, fut):
        ex = fut.exception()
        
        if ex != None:
            msg = "_onExecutionDone exception: %s\n full traceback:\n%s"%(str(ex),traceback.format_exc())
            self.logger.error(msg)
            self.signalError.emit(msg)


if __name__ == "__main__":
    pass