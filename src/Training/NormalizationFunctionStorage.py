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

def limitedNumericChangeNormalization(val):
    '''Translates limitedNumericChange values into a 0-200 range'''
    sign = 1
    if val < 0:
        sign = 0
    ret = abs(val) + (100 * sign)
    return ret

def limitedNumericChangeDenormalization(val):
    '''Translates values from a 0-200 range into limitedNumericChange values'''
    if val <= 100:
        ret = -val
    else:
        ret = val - 100
    return ret
