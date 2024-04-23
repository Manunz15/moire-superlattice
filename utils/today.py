# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import inflect
from datetime import date

def today() -> str:
    """
    TODAY
    -------------------------------------------------------------------------
    Return the current date in the format: 'd mmmm yyyy', with the day 
    expressed as an ordinal number. For example: '15th February 2002'.
    """

    p = inflect.engine()
    today_is = date.today()
    day = p.ordinal(int(today_is.strftime('%d')))
    return f'{day} {today_is.strftime("%B %Y")}'