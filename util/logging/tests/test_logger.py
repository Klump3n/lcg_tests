#!/usr/bin/env python3
"""
Test the string operations.

"""
import unittest

import sys
sys.path.append("..")
import logger
from logger import CoreLog

class Test_Logger(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_logger_with_name(self):
        """create logger with name
        """
        print()
        log = logger.BaseLogger("SOMENAME")

        log.info("no")
        log.debug("no")
        del log

    def test_logger_without_name(self):
        """create logger without name
        """
        print()
        log = logger.BaseLogger()
        log.info("no")
        log.debug("no")
        del log

    def test_logger_with_name_setlevel(self):
        """create logger with name and logging level
        """
        print()
        log = logger.BaseLogger("SOMENAME", "debug")

        log.info("no")
        log.debug("no")
        del log

    def test_mylogger(self):
        """mylogger

        """
        print()
        with self.assertRaises(ValueError):
            CoreLog.debug("hey")
        CoreLog("debug")
        CoreLog.info("hey")
        CoreLog()._clear()

    def test_mylogger_verbose(self):
        """verbose setting

        """
        print()
        CoreLog("debug")
        CoreLog.verbose("hey")
        CoreLog()._clear()

    def test_mylogger_notime(self):
        """without time

        """
        print()
        CoreLog("debug", time=False)
        CoreLog.verbose("hey")
        CoreLog()._clear()

    def test_mylogger_noname(self):
        """without name

        """
        print()
        CoreLog("debug", name="")
        CoreLog.verbose("hey")
        CoreLog()._clear()
        CoreLog("debug", name=None)
        CoreLog.verbose("hey")
        CoreLog()._clear()

    def test_mylogger_noname_notime(self):
        """without time and name

        """
        print()
        CoreLog("debug", name="", time=False)
        CoreLog.verbose("hey")
        CoreLog()._clear()

    def test_mylogger_debug(self):
        """debug setting

        """
        print()
        CoreLog("debug")
        CoreLog.debug("hey")
        CoreLog.verbose("hey")
        CoreLog.info("hey")
        CoreLog.warning("hey")
        CoreLog.error("hey")
        CoreLog.critical("hey")
        CoreLog.fatal("hey")
        CoreLog()._clear()

    def test_mylogger_verbose(self):
        """debug setting

        """
        print()
        CoreLog("verbose")
        CoreLog.debug("hey")
        CoreLog.verbose("hey")
        CoreLog.info("hey")
        CoreLog.warning("hey")
        CoreLog.error("hey")
        CoreLog.critical("hey")
        CoreLog()._clear()

    def test_mylogger_info(self):
        """debug setting

        """
        print()
        CoreLog("info")
        CoreLog.debug("hey")
        CoreLog.verbose("hey")
        CoreLog.info("hey")
        CoreLog.warning("hey")
        CoreLog.error("hey")
        CoreLog.critical("hey")
        CoreLog()._clear()

    def test_mylogger_warning(self):
        """debug setting

        """
        print()
        CoreLog("warning")
        CoreLog.debug("hey")
        CoreLog.verbose("hey")
        CoreLog.info("hey")
        CoreLog.warning("hey")
        CoreLog.error("hey")
        CoreLog.critical("hey")
        CoreLog()._clear()

    def test_mylogger_error(self):
        """debug setting

        """
        print()
        CoreLog("error")
        CoreLog.debug("hey")
        CoreLog.verbose("hey")
        CoreLog.info("hey")
        CoreLog.warning("hey")
        CoreLog.error("hey")
        CoreLog.critical("hey")
        CoreLog()._clear()

    def test_mylogger_critical(self):
        """debug setting

        """
        print()
        CoreLog("critical")
        CoreLog.debug("hey")
        CoreLog.verbose("hey")
        CoreLog.info("hey")
        CoreLog.warning("hey")
        CoreLog.error("hey")
        CoreLog.critical("hey")
        CoreLog()._clear()

    def test_mylogger_quiet(self):
        """debug setting

        """
        print()
        CoreLog("quiet")
        CoreLog.debug("hey")
        CoreLog.verbose("hey")
        CoreLog.info("hey")
        CoreLog.warning("hey")
        CoreLog.error("hey")
        CoreLog.critical("hey")
        CoreLog()._clear()

    def test_mylogger_fatal(self):
        """debug setting

        """
        print()
        CoreLog("fatal")
        CoreLog.debug("hey")
        CoreLog.verbose("hey")
        CoreLog.info("hey")
        CoreLog.warning("hey")
        CoreLog.error("hey")
        CoreLog.critical("hey")
        CoreLog()._clear()

if __name__ == '__main__':
    unittest.main(verbosity=2)

