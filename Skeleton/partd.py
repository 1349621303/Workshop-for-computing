import calendar
import csv
import time

"""
    Part C
    Please provide definitions for the following functions
"""

def time_convert(start_date, end_date):
    if isinstance(start_date, str) and isinstance(end_date, str):
        start = calendar.timegm(time.strptime(start_date, "%d/%m/%Y"))
        end = calendar.timegm(time.strptime(end_date, "%d/%m/%Y"))

        return start, end

def time_range_func(data, start, end):
    start_time, end_time = time_convert(start, end)
    range_data = []
    for d in data:
        time_stamp = int(d['time'])
        if start_time <= int(time_stamp) <= end_time:
            range_data.append(d)
    return range_data


def moving_avg_short(data, start_date, end_date):
    data_range = time_range_func(data, start_date, end_date)
    d_range = []
    for d in data_range:
        time_stamp = int(d['time'])
        d_range.append(time_stamp)

    avg_short = []
    for cur_i in range(0, len(d_range)):
        cur_time = d_range[cur_i]
        for whole_i in range(0, len(data)):
            pre_line = data[whole_i]
            whole_time = pre_line['time']

            if whole_i < 2 and cur_time == int(whole_time):
                # print("start_1")
                if whole_i == 0:
                    avg_short.append(round(float(pre_line['volumeto']) / float(pre_line['volumefrom']), 2))
                if whole_i == 1:
                    first_line = data[whole_i - 1]
                    first_rate = float(first_line['volumeto']) / float(first_line['volumefrom'])
                    second_rate = float(pre_line['volumeto']) / float(pre_line['volumefrom'])

                    avg_short.append(round((first_rate + second_rate) / 2, 2))

            elif cur_time == int(whole_time):
                pre_line_one = data[whole_i - 1]
                pre_line_two = data[whole_i - 2]

                divided = float(pre_line['volumeto']) / float(pre_line['volumefrom'])
                divided_one = float(pre_line_one['volumeto']) / float(pre_line_one['volumefrom'])
                divided_two = float(pre_line_two['volumeto']) / float(pre_line_two['volumefrom'])

                divided_sum = (divided + divided_one + divided_two) / 3
                avg_short.append(round(divided_sum, 2))

    return avg_short, d_range


def moving_avg_long(data, start_date, end_date):
    data_range = time_range_func(data, start_date, end_date)
    d_range = []
    for d in data_range:
        time_stamp = int(d['time'])
        d_range.append(time_stamp)

    avg_long_res = []

    for cur_i in range(0, len(d_range)):
        cur_time = d_range[cur_i]
        for whole_i in range(0, len(data)):
            pre_line = data[whole_i]

            if whole_i < 9 and cur_time == int(pre_line['time']):
                cur_less_sum = 0.0
                for i in range(whole_i):
                    cur_less_sum += (float(data[i]['volumeto']) / float(data[i]['volumefrom']))
                avg_long_res.append(round(cur_less_sum / whole_i, 2))

            elif whole_i >= 9 and cur_time == int(pre_line['time']):
                new_whole_i = whole_i
                cur_moving_sum = 0.0
                for i in range(new_whole_i-9, new_whole_i+1):
                    cur_moving_sum += (float(data[i]['volumeto']) / float(data[i]['volumefrom']))
                avg_long_res.append(round(cur_moving_sum / 10, 2))

    return avg_long_res


def find_buy_list(short_avg_dict, long_avg_dict):
    short_dict, data_range = short_avg_dict
    long_dict = long_avg_dict
    buy_list = []
    buy_list_date = []
    for s in range(1, len(data_range)):
        if short_dict[s-1] < long_dict[s-1] and short_dict[s] > long_dict[s]:
            buy_list.append(s)

    for date in buy_list:
        tup_time = time.localtime(data_range[date])
        time_str = time.strftime("%d/%m/%Y", tup_time)
        buy_list_date.append(time_str)
    return buy_list_date


def find_sell_list(short_avg_dict, long_avg_dict):
    short_dict, data_range = short_avg_dict
    long_dict = long_avg_dict

    sell_list = []
    sell_list_date = []
    for s in range(1, len(data_range)):
        # print(s)
        if short_dict[s-1] > long_dict[s-1] and short_dict[s] < long_dict[s]:
            sell_list.append(s)

    for date in sell_list:
        tup_time = time.localtime(data_range[date])
        time_str = time.strftime("%d/%m/%Y", tup_time)
        sell_list_date.append(time_str)
    return sell_list_date


def crossover_method(data, start_date, end_date):
    res_short = moving_avg_short(data, start_date, end_date)
    res_long = moving_avg_long(data, start_date, end_date)
    res_buy = find_buy_list(res_short, res_long)
    res_sell = find_sell_list(res_short, res_long)
    return res_buy, res_sell


if __name__ == "__main__":
    data = []
    with open("cryptocompare_btc.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

        # avg_long = moving_avg_long(data, "05/09/2018", "27/09/2018")
        # print(find_sell_list(moving_avg_short(data, "05/09/2018", "27/09/2018"), avg_long))

        # print(find_sell_list(moving_avg_short(data, "03/11/2019", "14/11/2019"), avg_long))

        # avg_long = moving_avg_long(data, "01/05/2017", "12/06/2017")
        # print(find_buy_list(moving_avg_short(data, "01/05/2017", "12/06/2017"), avg_long))

        buy, sell = crossover_method(data, "05/09/2018", "27/09/2018")
        print("Buy List is:", buy)
        print("Sell List is:", sell)


