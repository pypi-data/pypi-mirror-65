import os
from openProduction.common import Signals, misc, Exceptions
import logging
import traceback


class TestParams:
    DEVICE_ID = "deviceID"
    def __init__(self, params, folder=None):
        self.logger = logging.getLogger(misc.getAppName())
        self._params = params
        self._paramFolder = folder
        self._files = []
        self._children = []
        self.keyChanged = Signals.Signal()
        self.deviceIDSet = Signals.Signal()
        self._readOnly = False
        self._parent = None

    def __del__(self):
        self._delFiles()

    def getParent(self):
        return self._parent

    def setParent(self, obj):
        self._parent = obj

    def addChild(self, other):
        otherID = other.getDeviceID()

        #find highest parent
        obj = self
        while True:
            if obj.getParent() == None:
                break
            else:
                obj = obj.getParent()

        #search all children from highest point (assure a real global uniqueness)
        unique = obj._childIDUnique(otherID)
        if unique == False:
            raise Exceptions.DuplicateError("ID %s is not unique in container"%otherID)

        self._children.append(other)
        other.setParent(self)

    def getChildren(self):
        return self._children

    def getChild(self, otherID):
        for child in self._children:
            if child.getDeviceID() == otherID:
                return child
            val = child.getChild(otherID)
            if val != None:
                return val
        return None

    def _childIDUnique(self, otherID):
        isUnique = True
        try:
            myId = self.getDeviceID()
        except:
            myId = None

        if myId == otherID:
            return False

        for child in self.getChildren():
            isUnique = child._childIDUnique(otherID)
            if isUnique==False:
                break

        return isUnique

    def getFolder(self):
        return self._paramFolder        

    def setReadOnly(self, ro):
        self._readOnly = ro
        
    def removeKey(self, key):
        if self._readOnly:
            raise RuntimeError("remove key %s not allowed (TestParams is read-only)"%key)
        self._params.pop(key, None)
        
    def __getitem__(self, key):       
        return self._params[key]
    
    def __setitem__(self, key, value):
        if self._readOnly:
            raise RuntimeError("setting %s not allowed (TestParams is read-only)"%key)
            
        hasChanged = False
        if key not in self._params:
            hasChanged = True
        else:
            if value != self._params[key]:
                hasChanged = True

        self._params[key] = value
        
        if hasChanged:
            self.keyChanged.emit(key, value)
        if key == self.DEVICE_ID:
            self.deviceIDSet.emit(value)
        
    def __contains__(self, key):
        return key in self._params

    def setDeviceID(self, val):
        if self._readOnly:
            raise RuntimeError("setting deviceID not allowed (TestParams is read-only)")
        self._params[self.DEVICE_ID] = val
        self.deviceIDSet.emit(val)
        
    def getDeviceID(self):
        return self._params[self.DEVICE_ID]

    def _delFiles(self):
        for f in self._files:
            if f["deleteLocal"]:
                try:
                    os.remove(f["fname"])
                except:
                    self.logger.info("error deleting file %s"%f["fname"])
                    self.logger.error(traceback.format_exc())
        self._files = []

    def clear(self):
        self._params = {}
        self._delFiles()
        for child in self._children:
            child.clear()
        self._children = []
    
    def abspath(self, key):
        if self._paramFolder != None:
            return os.path.join(self._paramFolder, self._params[key])
        else:
            return self._params[key]
    
    def addFile(self, fileName, destFile=None, deleteLocal=False):
        if self._readOnly:
            raise RuntimeError("adding file not allowed (TestParams is read-only)")
        fName = os.path.abspath(fileName)
        fNames = [f["fname"] for f in self._files]
        if fName in fNames:
            raise RuntimeError("file %s already exists in params"%fName)
        if os.path.exists(fName) == False:
            raise RuntimeError("file %s doesn't exist"%fName)
        obj = {}
        obj["deleteLocal"] = deleteLocal
        obj["fname"] = fName
        if destFile == None:
            destFile = os.path.split(fileName)[-1]
        else:
            destFile = os.path.split(destFile)[-1]
        obj["destFilename"] = destFile
        self._files.append(obj)

    def getParams(self):
        return self._params
    
    def getFiles(self):
        return self._files
    
    def __len__(self):
        return len(self._params)
    
    def __str__(self):
        MAX_LEN = 40
        
        maxName = len("Name")
        maxValue = len("Value")
        
        for key, val in self._params.items():
            if type(val) == type({}):
                for subKey, subVal in val.items():
                    subKey = key+"."+subKey
                    maxName = max(maxName, len(subKey))
                    maxValue = max(maxValue, len(str(subVal)))
            else:
                maxName = max(maxName, len(key))
                maxValue = max(maxValue, len(str(val)))
            
        if maxName > MAX_LEN:
            maxName = MAX_LEN
        if maxValue > MAX_LEN:
            maxValue = MAX_LEN
            
        colName = maxName+2
        colVal = maxValue+2
        
        myStr = ""
        myStr += ("+"+"-"*colName + "+" + "-"*colVal + "+") + "\n"
        myStr += ("| Name " + " "*(colName-6) + "| Value " + " "*(colVal-7) + "|") + "\n"
        myStr += ("+"+"="*colName + "+" + "="*colVal + "+") + "\n"
        
        def toStrKeyVal(key,val):
            myStr = ""
            printKey = key
            if len(printKey)>MAX_LEN:
                printKey = printKey[:MAX_LEN-3]+"..."
            printVal = str(val)
            if len(printVal)>MAX_LEN:
                printVal = printVal[:MAX_LEN-3]+"..."
                
            myStr += ("| " + printKey + " "*(colName-len(printKey)-1) + "| " +
                      str(printVal) +" "*(colVal-len(str(printVal))-1) + "|" ) + "\n"
            myStr += ("+"+"-"*colName + "+" + "-"*colVal + "+") + "\n"
            return myStr
        
        for key, val in self._params.items():
            if type(val) == type({}):
                for subKey, subVal in val.items():
                    subKey = key+"."+subKey
                    myStr += toStrKeyVal(subKey, subVal)
            else:
                myStr += toStrKeyVal(key, val)
                
        for f in self._files:
            myStr += toStrKeyVal("**FILE**", f["fname"])
                
        return myStr