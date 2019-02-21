from Email.EClient import EClientFilter

devClientFilter = None


def _instantiateClientFilters():
    devClientFilter = EClientFilter()
    devClientFilter.addWhitelistEntry("prediction", [])
    devClientFilter.addWhitelistEntry("evaluation", [])
    



_instantiateClientFilters()