import csv
import re
import sys
import time
import calendar
"""
    Part B
    Please provide definitions for the following functions *WITH EXCEPTION HANDLERS*
"""

class RangeError(Exception):
    pass
class EndDateError(Exception):
    pass
class TimeFormatError(Exception):
    pass

def time_convert(start_date, end_date):
    if isinstance(start_date, int) and isinstance(end_date, int):
        try:
            if start_date < 1430179200 or end_date > 1602979200:
                raise TimeFormatError
        except TimeFormatError:
            print("Error: invalid date value")
            sys.exit()
        else:
            return start_date, end_date

    elif isinstance(start_date, str) and isinstance(end_date, str):
        date_reg_exp = re.compile('\d{2}/\d{2}/\d{4}')
        match_start = date_reg_exp.findall(start_date)
        match_end = date_reg_exp.findall(end_date)
        try:
            if len(match_start) == 0 or len(match_end) == 0:
                raise TimeFormatError
        except TimeFormatError:
            print("Error: invalid date value")
            sys.exit()
        else:
            start = calendar.timegm(time.strptime(start_date, "%d/%m/%Y"))
            end = calendar.timegm(time.strptime(end_date, "%d/%m/%Y"))

    try:
        if start < 1430179200 or end > 1602979200:
            raise RangeError
        elif start > end:
            raise EndDateError

    except RangeError:
        print("Error: date value is out of range")
        sys.exit()
    except EndDateError:
        print("Error: end date must be larger than start date")
        sys.exit()
    else:
        return start, end

def time_range_func(data, start, end):
    start_time, end_time = time_convert(start, end)
    range_data = []
    try:
        for d in data:
            time_stamp = int(d['time'])
            if start_time <= int(time_stamp) <= end_time:
                range_data.append(d)
    except KeyError:
        print("Error: requested column is missing from dataset")
        sys.exit(0)
    else:
        return range_data


# highest_price(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def highest_price(data, start_date, end_date):
    time_range = time_range_func(data, start_date, end_date)
    highest = 0
    for t in time_range:
        highest = max(highest, float(t['high']))
    return highest


# lowest_price(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def lowest_price(data, start_date, end_date):
    time_range = time_range_func(data, start_date, end_date)
    lowest = sys.maxsize

    for t in time_range:
        lowest = min(lowest, float(t['low']))
    return lowest


# max_volume(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def max_volume(data, start_date, end_date):
    time_range = time_range_func(data, start_date, end_date)
    volume = 0

    for t in time_range:
        volume = max(volume, float(t['volumefrom']))
    return volume


# best_avg_price(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def best_avg_price(data, start_date, end_date):
    time_range = time_range_func(data, start_date, end_date)
    best_avg = 0

    for t in time_range:
        best_avg = max(best_avg, (float(t['volumeto']) / float(t['volumefrom'])))
    return best_avg


# moving_average(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def moving_average(data, start_date, end_date):
    time_range = time_range_func(data, start_date, end_date)
    moving_sum = 0
    moving_index = 0

    for t in time_range:
        moving_index += 1
        moving_sum += float(t['volumeto']) / float(t['volumefrom'])
    res = moving_sum / moving_index
    return round(res, 2)


# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    data = []
    try:
        f = open("cryptocompare_btc.csv", "r")
    except FileNotFoundError:
        print("Error: dataset not found")
    else:
        reader = csv.DictReader(f)
        data = [r for r in reader]

        # test highest
        print(moving_average(data, "01/01/2016", "31/01/2016"))
