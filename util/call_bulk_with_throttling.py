import time


def call_bulk_with_throttling(func, max_calls, sleep_time, args_arr):
    calls = 0
    array_length = len(args_arr)
    for i in range(array_length):
        func(args_arr[i])
        calls += 1
        if calls >= max_calls and i < array_length - 1:
            time.sleep(sleep_time)
            calls = 0
