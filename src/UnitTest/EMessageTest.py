from EmailUtils.EMessage import EMessage
from unittest import TestCase

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

class EMessageTest(TestCase):
    
    def testCreation(self):
        msg1 = EMessage(msg1Body, msg1Identifier, msg1Subject, [])
        msg2 = EMessage(msg2Body, msg2Identifier, msg2Subject, [])
        self.assertEqual(msg2.body, msg2Body)
        self.assertEqual(msg2.subject, msg2Subject)
        self.assertEqual(msg2.identifier, msg2Identifier)
        self.assertEqual(msg1.identifier, msg1Identifier)
        self.assertEqual(msg1.subject, msg1Subject)
        self.assertEqual(msg1.body, msg1Body)

        self.assertNotEqual(msg2.body, msg1.body)
