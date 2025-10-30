from datetime import datetime
import calendar

def print_current_month():
    now = datetime.now()
    year = now.year
    month = now.month
    print(calendar.month(year, month))


if __name__ == "__main__":
    print_current_month()
