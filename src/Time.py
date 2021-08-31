import datetime

def time():
    now = datetime.datetime.now()
    num = now.strftime('_%Y%m%d_%H%M%S')
    version = str(num)
    return version

