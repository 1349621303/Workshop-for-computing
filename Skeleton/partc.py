import calendar
import re
import sys
import csv
import time

"""
    Part D
    Please provide definitions for the following class and functions
"""

class Investment:
    data = None
    start_date = None
    end_date = None
    def __init__(self, data, start_date, end_date):
        self.data = data
        self.start_date = start_date
        self.end_date = end_date


    def time_convert(self):
        if isinstance(self.start_date, int) and isinstance(self.end_date, int):
            try:
                if self.start_date < 1430179200 or self.end_date > 1602979200:
                    raise TimeFormatError
            except TimeFormatError:
                print("Error: invalid date value")
                sys.exit()
            else:
                return self.start_date, self.end_date

        elif isinstance(self.start_date, str) and isinstance(self.end_date, str):
            date_reg_exp = re.compile('\d{2}/\d{2}/\d{4}')
            match_start = date_reg_exp.findall(self.start_date)
            match_end = date_reg_exp.findall(self.end_date)
            try:
                if len(match_start) == 0 or len(match_end) == 0:
                    raise TimeFormatError
            except TimeFormatError:
                print("Error: invalid date value")
                sys.exit()
            else:
                start = calendar.timegm(time.strptime(self.start_date, "%d/%m/%Y"))
                end = calendar.timegm(time.strptime(self.end_date, "%d/%m/%Y"))

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
    pass


    def time_range_func(self):
        start_time, end_time = self.time_convert()
        range_data = []
        try:
            for d in self.data:
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
    def highest_price(self):
        time_range = self.time_range_func()
        highest = 0
        for t in time_range:
            highest = max(highest, float(t['high']))
        return highest

    # lowest_price(data, start_date, end_date) -> float
    # data: the data from a csv file
    # start_date: string in "dd/mm/yyyy" format
    # start_date: string in "dd/mm/yyyy" format
    def lowest_price(self):
        time_range = self.time_range_func()
        lowest = sys.maxsize

        for t in time_range:
            lowest = min(lowest, float(t['low']))
        return lowest

    # max_volume(data, start_date, end_date) -> float
    # data: the data from a csv file
    # start_date: string in "dd/mm/yyyy" format
    # start_date: string in "dd/mm/yyyy" format
    def max_volume(self):
        time_range = self.time_range_func()
        volume = 0

        for t in time_range:
            volume = max(volume, float(t['volumefrom']))
        return volume

    # best_avg_price(data, start_date, end_date) -> float
    # data: the data from a csv file
    # start_date: string in "dd/mm/yyyy" format
    # start_date: string in "dd/mm/yyyy" format
    def best_avg_price(self):
        time_range = self.time_range_func()
        best_avg = 0

        for t in time_range:
            best_avg = max(best_avg, (float(t['volumeto']) / float(t['volumefrom'])))
        return best_avg

    # moving_average(data, start_date, end_date) -> float
    # data: the data from a csv file
    # start_date: string in "dd/mm/yyyy" format
    # start_date: string in "dd/mm/yyyy" format
    def moving_average(self):
        time_range = self.time_range_func()
        moving_sum = 0
        moving_index = 0

        for t in time_range:
            moving_index += 1
            moving_sum += float(t['volumeto']) / float(t['volumefrom'])
        res = moving_sum / moving_index
        return round(res, 2)


def avg_x(data):
    x_len = len(data)
    x_sum = 0
    for x in data:
        x_sum += x
    return x_sum / x_len


def avg_y(data):
    y_len = len(data)
    y_sum = 0
    for y in data:
        y_sum += y
    return y_sum / y_len


def linear_regression_down(list_x):
    linear_avg_x = avg_x(list_x)
    linear_sum = 0
    for x_item in list_x:
        linear_sum += (x_item - linear_avg_x) ** 2
    return linear_sum

def linear_regression_up(list_x, list_y):
    linear_avg_x = avg_x(list_x)
    linear_avg_y = avg_y(list_y)
    all_sum = 0
    for x_item, y_item in zip(list_x, list_y):
        all_sum += (x_item - linear_avg_x) * (y_item - linear_avg_y)
    return all_sum

def linear_regression_b_one(list_x, list_y):
    return linear_regression_up(list_x, list_y) / linear_regression_down(list_x)

def linear_regression_b_zero(list_x, list_y):
    linear_avg_x = avg_x(list_x)
    linear_avg_y = avg_y(list_y)
    return linear_avg_y - linear_regression_b_one(list_x, list_y) * linear_avg_x


# predict_next_average(investment) -> float
# investment: Investment type
def predict_next_average(investment):
    predict_list = investment.time_range_func()
    x_list = []
    y_list = []
    pre_list_len = len(predict_list)
    for i in range(pre_list_len):
        cur_line = predict_list[i]
        x_list.append(int(cur_line['time']))
        y_list.append(float(cur_line['volumeto'])/float(cur_line['volumefrom']))
    # print(y_list)
    b_one = linear_regression_b_one(x_list, y_list)
    # print(b_one)
    b_zero = linear_regression_b_zero(x_list, y_list)
    # print(b_zero)
    predict_x = 0
    data_len = len(investment.data)
    # print(x_list[-1])
    for i in range(data_len):
        cur = investment.data[i]
        if int(cur['time']) == x_list[-1]:
            # print(float(investment.data[i+1]['time']))
            next_day = investment.data[i+1]
            predict_x = (float)(next_day['time'])

    predict_y = b_one * predict_x + b_zero

    return predict_y


# classify_trend(investment) -> str
# investment: Investment type
def classify_trend(investment):
    classify_list = investment.time_range_func()
    lowest_list_x = []
    lowest_list_y = []
    highest_list_x = []
    highest_list_y = []
    classify_list_len = len(classify_list)
    for i in range(classify_list_len):
        cur_line = classify_list[i]
        lowest_list_x.append(int(cur_line['time']))
        lowest_list_y.append(float(cur_line['low']))
        highest_list_x.append(int(cur_line['time']))
        highest_list_y.append(float(cur_line['high']))

    low_b_one = linear_regression_b_one(lowest_list_x, lowest_list_y)
    # low_b_zero = linear_regression_b_zero(lowest_list_x, lowest_list_y)

    high_b_one = linear_regression_b_one(highest_list_x, highest_list_y)
    # high_b_zero = linear_regression_b_zero(highest_list_x, highest_list_y)

    if high_b_one > 0 and low_b_one < 0:
        res = "volatile"
    elif high_b_one > 0 and low_b_one > 0:
        res = "increasing"
    elif high_b_one < 0 and low_b_one < 0:
        res = "decreasing"
    else:
        res = "other"
    return res

class RangeError(Exception):
    pass

class EndDateError(Exception):
    pass

class TimeFormatError(Exception):
    pass

# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program
    data = []
    with open("cryptocompare_btc.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    investment = Investment(data, '08/12/2016', '11/12/2016')

    print(predict_next_average(investment))
    # print(predict_next_average(investment))
    print(classify_trend(investment))

    pass