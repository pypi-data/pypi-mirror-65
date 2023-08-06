import time


def string_to_stamp(timestring, tformat):
    return int(time.mktime(time.strptime(timestring, tformat)))


def stamp_to_string(timestamp, tformat):
    time_array = time.localtime(timestamp)
    return time.strftime(tformat, time_array)
