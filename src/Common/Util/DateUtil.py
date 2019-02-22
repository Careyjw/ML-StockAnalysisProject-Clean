from datetime import date, datetime


def dateToTimestamp(Date : 'date'):
    x = Date.strftime('%Y-%m-%d')
    v = datetime.strptime(x, '%Y-%m-%d')
    return v.timestamp()