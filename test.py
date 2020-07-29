from datetime import datetime

import locale
import platform

if platform.system() == "Windows":
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, "ru_RU") 

def parse_autonews_date(date_str):
    dates = {
        "января" : "январь",
        "февраля" : "февраль",
        "марта" : "март",
        "апреля" : "апрель",
        "мая" : "май",
        "июня" : "июнь",
        "июля" : "июль",
        "августа" : "август",
        "сентября" : "сентябрь",
        "октября" : "октябрь",
        "ноября" : "ноябрь",
        "декабря" : "декабрь",
    }
    date_str = date_str.lower()
    for month in dates.keys():
        if month in date_str:
            date_str = date_str.replace(month, dates.get(month))
    
    try: 
        date_str = datetime.strptime(date_str, "%d %B %Y")
    except ValueError:
        curr_date = datetime.now()
        curr_year = datetime.strftime(curr_date, " %Y")
        date_str += curr_year
        date_str = datetime.strptime(date_str, "%d %B %Y")
    except:
        date_str = datetime.now()

    return datetime.strftime(date_str, "%d/%B/%Y")

print(parse_autonews_date("12 сентября 1999"))