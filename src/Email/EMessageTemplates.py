from Email.EMessage import EMessage

devTickerPredEM : "EMessage" = None

def _initializeMessageTemplates():
    global devTickerPredEM
    devTickerPredEM = EMessage(
    '''Hello {customer},
Here is your prediction results for today:

{ticker}

Have a nice day''', "prediction", "Daily Prediction Results", [], defaultMessageStatus=False)

_initializeMessageTemplates()



