

def movementDirectionNormalization(val):
    if val == "stag":
        return 0
    elif val == "up":
        return 1
    else:
        return 2

def movementDirectionDenormalization(val):
    if val == 0:
        return "stag"
    elif val == 1:
        return "up"
    else:
        return "down"