import datetime

def actual_year(request):
    return {'actual_year': datetime.datetime.now().strftime("%Y")}