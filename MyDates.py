


import datetime as dt
from numpy import floor




def eomonth(enter_date, months):
    new_month = int((((enter_date.month - 1) + months + 1) % 12) + 1)
    new_year = int(enter_date.year + floor((enter_date.month + months) / 12))
    end_of_month = dt.date(new_year, new_month, 1) - dt.timedelta(days=1)
    return end_of_month
    
