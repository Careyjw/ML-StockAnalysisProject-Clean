from unittest import TestCase
from Common.Util.CommonFunctions import config_handling, loginCredentialAssembling


class LoginCredentialAssemblingTest(TestCase):

    def testAssembling(self):
        config = config_handling()
        password = "Test"
        test = loginCredentialAssembling(password)
        self.assertEqual(config[0], test[0])
        self.assertEqual(config[1], test[1])
        self.assertEqual(config[3], test[3])
        self.assertEqual(password, test[2])