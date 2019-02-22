from Email.EMessage import EMessage

devTickerPredEM : "EMessage" = None
devTickerEvalEM : "EMessage" = None

def _initializeMessageTemplates():
    global devTickerPredEM
    global devTickerEvalEM
    devTickerPredEM = EMessage(
    '''Hello {customer},
Here is your prediction results for today:

{ticker}

Have a nice day''', "prediction", "Daily Prediction Results", [], defaultMessageStatus=False)
    devTickerEvalEM = EMessage(
    '''Hello {customer},
Here is your evaluation results for today:

{ticker}

Have a nice day''', "evaluation", "Daily Prediction Results", [], defaultMessageStatus=False)

_initializeMessageTemplates()



