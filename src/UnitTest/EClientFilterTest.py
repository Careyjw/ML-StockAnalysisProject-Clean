from Email.EClient import EClientFilter, FilterCombinationError
from Email.EMessage import EMessage
import unittest

msg1Body = '''Hello {customer},
{ticker}
Have a nice day!'''
msg1Subject = "StockDataPredictions"
msg1Identifier = "TickerData"

msg2Body = '''Hello {customer},
    This is an automated message to inform you that
you have been registered for automated emails
from our service. If this is not the case,
please respond to this email to inform us
that you are not interested in receiving
these emails.
Have a nice day!'''
msg2Subject = "Registration Notification"
msg2Identifier = "Registration"




class EClientFilterTest(unittest.TestCase):

    def setUp(self):
        self.msg1 = EMessage(msg1Body, msg1Identifier, msg1Subject, [])
        self.msg2 = EMessage(msg2Body, msg2Identifier, msg2Subject, [])
        self.filter1 = EClientFilter()
        self.filter2 = EClientFilter()
        self.filter3 = EClientFilter()
        self.filter4 = EClientFilter()
        
        self.filter1.addWhitelistEntry("Registration", ["Dev"])
        self.filter2.addWhitelistEntry("Registration", [])
        self.filter3.addBlacklistEntry("Registration", ["Dev"])
        self.filter4.addBlacklistEntry("Registration", [])

        self.filter1.addBlacklistEntry("TickerData", [])


    def testCombine(self):
        filterIdent1 = EClientFilter.EClientFilterIdentifier("Registration", ["Dev"])
        filterIdent2 = EClientFilter.EClientFilterIdentifier("Registration", [])
        filterIdent3 = EClientFilter.EClientFilterIdentifier("TickerData", [])
        
        filtIdents = [filterIdent1, filterIdent2, filterIdent3]

        resFilt = self.filter1 + self.filter2

        self.assertIn(filterIdent1, resFilt.whitelistIdentifiers)
        self.assertIn(filterIdent2, resFilt.whitelistIdentifiers)
        self.assertIn(filterIdent3, resFilt.blacklistIdentifiers)

    
        with self.assertRaises(FilterCombinationError):
            resFilt = self.filter1 + self.filter3

    
    def testFiltering(self):
        self.assertFalse(self.filter1.filterMessage(self.msg2))
        self.assertTrue(self.filter2.filterMessage(self.msg2))
        self.assertFalse(self.filter3.filterMessage(self.msg2))
        self.assertFalse(self.filter4.filterMessage(self.msg2))
        
        self.assertFalse(self.filter1.filterMessage(self.msg1))
        self.assertFalse(self.filter2.filterMessage(self.msg1))
        self.assertFalse(self.filter3.filterMessage(self.msg1))
        self.assertFalse(self.filter4.filterMessage(self.msg1))
