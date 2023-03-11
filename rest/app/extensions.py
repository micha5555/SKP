import datetime

def tokenAdminRequire():
    pass

def tokenControlerRequire():
    pass

def createToken():
    pass

def getDataFromToken():
    pass

# We get time from UTC,, but we need Poland time zone so we need to add +1 to hour
def createDatetime(string):
    dt_utc = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
    dt_local = dt_utc.astimezone(datetime.timezone(datetime.timedelta(hours=1)))
    return dt_local

# We get current time from UTC,, but we need Poland time zone so we need to add +1 to hour
def getDatetimeNow():
    dt_utc = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    dt_local = dt_utc.astimezone(datetime.timezone(datetime.timedelta(hours=1)))
    return dt_local