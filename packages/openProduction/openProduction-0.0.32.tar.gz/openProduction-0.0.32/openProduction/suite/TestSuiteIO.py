from enum import Enum
from openProduction.common import Signals, Exceptions
import os
import winsound
import threading

class ImageFormat(Enum):
    GRAYSCALE_8 = 0
    RGB_888 = 1
    BGR_888 = 2

class IOAnswer(Enum):
    YES = 0
    NO = 1
    CANCEL = 2
    TIMEOUT = 3
    RETRY = 4

class BaseIOHandler:
    def __init__(self):
        self.signalMessage = Signals.Signal()
        self._abort_event = threading.Event()
        
    def _queryYesNo(self, title, msg):
        return IOAnswer.CANCEL
        
    def _queryYesNoRetry(self, title, msg, retry):
        return IOAnswer.CANCEL

    def _plot(self, *args, **kwargs):
        pass
    
    def newImageData(self, image, imageType):
        pass
    
    def message(self, msg):
        self.signalMessage.emit(msg)    
    
    #############################################
    # Methods below should not be overwritten ! #
    #############################################
    def plot(self, *args, **kwargs):
        if self._abort_event.is_set():
            raise Exceptions.OpenProductionAbortError("")
        else:
            self._plot(*args, **kwargs)
        
    def abort(self):
        self._abort_event.set()
        
    def abortClear(self):
        self._abort_event.clear()        

    def queryYesNo(self, title, msg):
        if self._abort_event.is_set():
            raise Exceptions.OpenProductionAbortError("")
        else:
            rv =  self._queryYesNo(title, msg)
            if rv == IOAnswer.CANCEL:
                raise Exceptions.OpenProductionAbortError("")
            else:
                return rv

    def queryYesNoRetry(self, title, msg, retry):
        if self._abort_event.is_set():
            raise Exceptions.OpenProductionAbortError("")
        else:
            rv =  self._queryYesNoRetry(title, msg, retry)
            if rv == IOAnswer.CANCEL:
                raise Exceptions.OpenProductionAbortError("")
            else:
                return rv
        
    def playNotify(self):
        if self._abort_event.is_set():
            raise Exceptions.OpenProductionAbortError("")
        myPath = os.path.split(os.path.abspath(__file__))[0]
        soundPath = os.path.abspath(os.path.join(myPath, "../UI/qml/sound/notify.wav"))
        try:
            winsound.PlaySound(soundPath, winsound.SND_FILENAME)
        except:
            pass
        
    def playError(self):
        if self._abort_event.is_set():
            raise Exceptions.OpenProductionAbortError("")
        myPath = os.path.split(os.path.abspath(__file__))[0]
        soundPath = os.path.abspath(os.path.join(myPath, "../UI/qml/sound/error.wav"))
        try:
            winsound.PlaySound(soundPath, winsound.SND_FILENAME)
        except:
            pass
        
    def playSuccess(self):
        if self._abort_event.is_set():
            raise Exceptions.OpenProductionAbortError("")
        myPath = os.path.split(os.path.abspath(__file__))[0]
        soundPath = os.path.abspath(os.path.join(myPath, "../UI/qml/sound/success.wav"))
        try:
            winsound.PlaySound(soundPath, winsound.SND_FILENAME)
        except:
            pass               

class IOMessage:
    def __init__(self, msg):
        self.msg = msg
