from openProduction.suite import TestSuite, TestParams
from openProduction.product import ProductExecutor
from openProduction.station import Station
from openProduction.common import misc
from openProduction.connectors.BaseConnector import ConnectorErrors
import logging 

class ResultConnector(ProductExecutor.ProductExecutor):
    """Result connector setup hooks"""
    
    def __init__(self, ctor):
        super(ResultConnector, self).__init__(ctor)
        self.logger = logging.getLogger(misc.getAppName())
        self.station = Station.Station.getInstance()
        
        if self.station != None:
            self.stationName = self.station.stationName
            
    def installRunner(self, runner):
        self.testSuiteRunner = runner
        
    def install(self, testSuite):
        hint = TestSuite.InstallHints(shouldBeLast=True)
        testSuite.addMethodHint(self.teardown_result_00100, hint)
        self.testSuite = testSuite

    def _transmitValue(self, params, value, parentID):
        result_id = None

        if "NO_LOG_RESULTS" not in params:
            f = open("log.txt", "w")
            f.write(self.testSuiteRunner.suiteResults.getLogText())
            f.close()
            value.addFile("log.txt")

        if "sftp_config_id" in params:
            sftp_config_id = params["sftp_config_id"]
        else:
            sftp_config_id = 1

        data = {}
        data["revision_id"] = self.station.loadedProduct.version.revision
        data["station_id"] = self.station.stationID
        data["result"] = value.getParams()
        data["duration"] = self.testSuiteRunner.suiteResults.executionTime
        data["testCaseResults"] = self.testSuiteRunner.suiteResults.toDict()
        data["openProductionVersion"] = misc.getVersion()
        data["success"] = self.testSuiteRunner.suiteResults.isSuccessful()
        data["deviceID"]  = value.getDeviceID()
        data["tempParams"] = self.tempParams.getParams()
        data["parent"] = parentID
        data["sftp_config_id"] = sftp_config_id

        data["result"].pop(value.DEVICE_ID, None)
        self.logger.info("Übertrage Ergebnisse")
        rv, data = self.station.serverIF.createProductResult(data)
        if rv == ConnectorErrors.NO_ERROR:
            result_id = data["product_result_id"]
            value["product_result_id"] = result_id
            self.logger.info("... ok (product_result_id=%d)"%result_id)
            
            for f in value.getFiles():
                srcFile = f["fname"]
                dstFile = f["destFilename"]
                data = {"result_id":result_id, "filename": srcFile, "destFilename": dstFile, "sftp_config_id": sftp_config_id}
                rv = self.station.serverIF.createProductResultFile(data)
                self.logger.info("Übertrage Datei %s"%srcFile)
                if rv != ConnectorErrors.NO_ERROR:
                    break

        return rv, result_id

    def _transmitRecursive(self, params, values, parentID):
        rv, result_id = self._transmitValue(params, values, parentID)
        if rv == ConnectorErrors.NO_ERROR:
            parentID = result_id
            for val in values.getChildren():
                rv, result_id = self._transmitRecursive(params, val, parentID)
                if rv != ConnectorErrors.NO_ERROR:
                    break
        return rv, result_id

    def teardown_result_00100(self, params, values):
        """Durchlaufergebnisse ablegen"""
        if self.station != None and self.station.loadedProduct != None:
            if "NO_TRANSMIT_RESULTS" in params:
                self.logger.info("Skippe Erbenisübertragung, 'NO_TRANSMIT_RESULTS' in params gesetzt, Parameter sind:")
                self.logger.info(str(values))
                return TestSuite.ExecutionResult.SKIP
            else:

                parentID = None
                self.station.serverIF.startTransaction()

                try:
                    rv, parentID = self._transmitRecursive(params, values, None)
                    self.assertEqual(rv, ConnectorErrors.NO_ERROR, "Fehler beim Übertragen der Ergebnisse: %s"%rv.name, ignoreAbort=True)
                except:
                    self.station.serverIF.rollbackTransaction()
                    raise

                self.station.serverIF.commitTransaction()


        else:
            if self.station == None:
                self.logger.info("Skippe Ergebnisübertragung, station=None")
            else:
                self.logger.info("Skippe Ergebnisübertragung, station.loadedProduct=None")
            return TestSuite.ExecutionResult.SKIP
        