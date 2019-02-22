class CaselessDictionary:
    '''A dictionary that translates all keys to lowercase strings'''


    def __init__(self):
        self.dict = {}

    def __getitem__(self, key : str):
        return self.dict[key.lower()]

    def __setitem__(self, key : str, item):
        self.dict[key.lower()] = item

    def items(self):
        return self.dict.items()

    def __str__(self):
        return str(self.dict)
    
    def __repr__(self):
        return repr(self.dict)