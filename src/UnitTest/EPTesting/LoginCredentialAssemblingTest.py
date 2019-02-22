from unittest import TestCase
from Common.Util.CommonFunctions import config_handling, loginCredentialAssembling


class LoginCredentialAssemblingTest(TestCase):

    def testAssembling(self):
        config = config_handling()
        password = "Test"
        test = loginCredentialAssembling(password)
        self.assertEqual(config[0], test[0])
        self.assertEqual(config[1], test[1])
        self.assertEqual(config[2], test[2])
        self.assertEqual(password, test[3])