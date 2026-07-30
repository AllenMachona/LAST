from datetime import datetime

_counter = 0

def generate_tender_number():
    global _counter
    _counter += 1
    year = datetime.now().year
    return f"BWP-EBMS-{year}-{_counter:05d}"
