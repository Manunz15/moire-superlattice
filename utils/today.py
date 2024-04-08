# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from datetime import date
import inflect

def today():
    p = inflect.engine()
    today_is = date.today()
    day = p.ordinal(int(today_is.strftime('%d')))
    return f'{day} {today_is.strftime("%B %Y")}'