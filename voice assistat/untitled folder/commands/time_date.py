import datetime

def current_time():
    now = datetime.datetime.now()
    print("Current Time:", now.strftime("%H:%M"))
    return now.time()

def current_date():
    now = datetime.datetime.now()
    print("Current Date:", now.strftime("%Y-%m-%d"))
    return now.date()

def current_day():
    now = datetime.datetime.now()
    print("Today is:", now.strftime("%A"))
    return now.strftime("%A")

def current_month():
    now = datetime.datetime.now()
    print("Current Month:", now.strftime("%B"))
    return now.strftime("%B")
def currrent_day():
    now = datetime.datetime.now()
    print("Current Day:", now.strftime("%d"))
    return now.strftime("%d")
def current_year():
    now = datetime.datetime.now()
    print("Current Year:", now.strftime("%Y"))
    return now.strftime("%Y")