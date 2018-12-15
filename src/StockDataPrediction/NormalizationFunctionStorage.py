def movementDirectionNormalization(val):
    '''Translates movementDirection values into a 0-2 range
    '''
    if val == "stag":
        return 0
    elif val == "up":
        return 1
    else:
        return 2

def movementDirectionDenormalization(val):
    '''Translates a value in the range 0-2 into movementDirection Values
    '''
    if val == 0:
        return "stag"
    elif val == 1:
        return "up"
    else:
        return "down"