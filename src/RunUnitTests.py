import unittest

from UnitTest import EClientFilterTest
from UnitTest import EMessageTest
from UnitTest.EPTesting import LoginCredentialAssemblingTest

class FailedTestError(Exception):
    pass

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromModule(EClientFilterTest))
    suite.addTest(loader.loadTestsFromModule(EMessageTest))
    suite.addTest(loader.loadTestsFromModule(LoginCredentialAssemblingTest))

    runner = unittest.TextTestRunner(verbosity=3)
    res = runner.run(suite)
    if (len(res.errors) > 0):
        exit(1)