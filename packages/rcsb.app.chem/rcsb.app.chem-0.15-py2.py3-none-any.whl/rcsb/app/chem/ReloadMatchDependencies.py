##
# File:    ReloadMatchDependencies.py
# Author:  J. Westbrook
# Date:    15-Mar-2020
# Version: 0.001
#
# Update:
#
#
##
"""
Fixture to prepare data dependencies for ChemCompSearchWrapper()

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import platform
import resource
import time

from rcsb.utils.chem.ChemCompSearchWrapper import ChemCompSearchWrapper
from rcsb.utils.io.MarshalUtil import MarshalUtil


HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ReloadMatchDependencies(object):
    def __init__(self):
        self.__startTime = time.time()
        self.__cachePath = os.environ.get("CHEM_SEARCH_CACHE_PATH", "./CACHE")
        ccFileNamePrefix = os.environ.get("CHEM_SEARCH_CC_PREFIX", "cc-abbrev")
        configFlagFull = ccFileNamePrefix == "cc-full"
        self.__dataPath = os.path.join(TOPDIR, "rcsb", "app", "tests-chem", "test-data")
        # Create the bootstrap configuration
        self.__mU = MarshalUtil(workPath=self.__cachePath)
        self.__makeBootstrapConfig(configFlagFull)
        logger.info("Starting at %s", time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def shutdown(self):
        unitS = "MB" if platform.system() == "Darwin" else "GB"
        rusageMax = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        logger.info("Maximum resident memory size %.4f %s", rusageMax / 10 ** 6, unitS)
        endTime = time.time()
        logger.info("Completed at %s (%.4f seconds)", time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def __makeBootstrapConfig(self, configFlagFull):
        """ Create search configuration bootstrap files
        """
        ok = False
        try:
            if configFlagFull:

                os.environ["CHEM_SEARCH_CACHE_PATH"] = os.path.join(self.__cachePath)
                os.environ["CHEM_SEARCH_CC_PREFIX"] = "cc-full"
                ccFileNamePrefix = "cc-full"
                configDirPath = os.path.join(self.__cachePath, "config")
                configFilePath = os.path.join(configDirPath, ccFileNamePrefix + "-config.json")
                oeFileNamePrefix = "oe-full"
                ccFileNamePrefix = "cc-full"
                ccUrlTarget = None
                birdUrlTarget = None

            else:
                os.environ["CHEM_SEARCH_CACHE_PATH"] = os.path.join(self.__cachePath)
                os.environ["CHEM_SEARCH_CC_PREFIX"] = "cc-abbrev"
                ccUrlTarget = os.path.join(self.__dataPath, "components-abbrev.cif")
                birdUrlTarget = os.path.join(self.__dataPath, "prdcc-abbrev.cif")
                ccFileNamePrefix = "cc-abbrev"
                configDirPath = os.path.join(self.__cachePath, "config")
                configFilePath = os.path.join(configDirPath, ccFileNamePrefix + "-config.json")
                oeFileNamePrefix = "oe-abbrev"
            #
            logger.info("Updating configuration using %s and %s", ccFileNamePrefix, self.__cachePath)
            molLimit = None
            useCache = False
            logSizes = False
            #
            numProc = 12
            maxProc = os.cpu_count()
            numProc = min(numProc, maxProc)
            maxChunkSize = 10
            logger.info("+++ >>> Using MAXPROC %d", numProc)
            #
            limitPerceptions = False
            quietFlag = True
            #
            # fpTypeCuttoffD = {"TREE": 0.6, "MACCS": 0.9, "PATH": 0.6, "CIRCULAR": 0.6, "LINGO": 0.9}
            fpTypeCuttoffD = {"TREE": 0.6, "MACCS": 0.9}
            buildTypeList = ["oe-iso-smiles", "oe-smiles", "cactvs-iso-smiles", "cactvs-smiles", "inchi"]
            #
            oesmpKwargs = {
                "ccUrlTarget": ccUrlTarget,
                "birdUrlTarget": birdUrlTarget,
                "cachePath": self.__cachePath,
                "useCache": useCache,
                "ccFileNamePrefix": ccFileNamePrefix,
                "oeFileNamePrefix": oeFileNamePrefix,
                "limitPerceptions": limitPerceptions,
                "minCount": None,
                "maxFpResults": 50,
                "fpTypeCuttoffD": fpTypeCuttoffD,
                "buildTypeList": buildTypeList,
                "screenTypeList": None,
                "quietFlag": quietFlag,
                "numProc": numProc,
                "maxChunkSize": maxChunkSize,
                "molLimit": molLimit,
                "logSizes": logSizes,
            }
            ccsiKwargs = {
                "ccUrlTarget": ccUrlTarget,
                "birdUrlTarget": birdUrlTarget,
                "cachePath": self.__cachePath,
                "useCache": useCache,
                "ccFileNamePrefix": ccFileNamePrefix,
                "oeFileNamePrefix": oeFileNamePrefix,
                "limitPerceptions": limitPerceptions,
                "minCount": None,
                "numProc": numProc,
                "quietFlag": quietFlag,
                "maxChunkSize": maxChunkSize,
                "molLimit": None,
                "logSizes": False,
            }
            configD = {"versionNumber": 0.20, "ccsiKwargs": ccsiKwargs, "oesmpKwargs": oesmpKwargs}
            self.__mU.mkdir(configDirPath)
            ok = self.__mU.doExport(configFilePath, configD, fmt="json", indent=3)
            return ok
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return ok

    def updateDependencies(self):
        """Test update search index.
        """
        try:
            logger.info("Starting update %r in %r", os.environ["CHEM_SEARCH_CC_PREFIX"], os.environ["CHEM_SEARCH_CACHE_PATH"])
            ccsw = ChemCompSearchWrapper()
            ok1 = ccsw.readConfig()
            ok2 = ccsw.updateChemCompIndex()
            ok3 = ccsw.updateSearchIndex()
            ok4 = ccsw.updateSearchMoleculeProvider()
            # verify access -
            ok5 = ccsw.reloadSearchDatabase()
            return ok1 and ok2 and ok3 and ok4 and ok5
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return False


if __name__ == "__main__":
    rmd = ReloadMatchDependencies()
    rmd.updateDependencies()
    rmd.shutdown()
