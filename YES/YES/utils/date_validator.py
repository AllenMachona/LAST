from datetime import datetime, timedelta
import pytz

def format_botswana_time(value):
    if value is None:
        return ''
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except:
            return value
    return value.strftime('%d %b %Y %H:%M') + ' CAT'

def is_business_day(date):
    return date.weekday() < 5

def add_business_days(start_date, days):
    current = start_date
    while days > 0:
        current += timedelta(days=1)
        if is_business_day(current):
            days -= 1
    return current
