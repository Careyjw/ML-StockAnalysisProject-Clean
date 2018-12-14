from EmailUtils.EClient import EClientFilter

devClientFilter = None


def _instantiateClientFilters():
    devClientFilter = EClientFilter()
    devClientFilter.addWhitelistEntry("prediction", [])
    



_instantiateClientFilters()