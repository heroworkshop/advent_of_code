from contextlib import suppress
from functools import reduce

from aocd_tools import load_input_data


def valid_buses(line):
    return [x for x in line.split(",") if x != "x"]


def offsets(buses):
    result = {}
    for offset, bus in enumerate(buses):
        with suppress(ValueError):
            result[int(bus)] = offset
    return result


def run():
    input_data = load_input_data(2020, 13)
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = input_data.split("\n")
    start_time = int(lines[0])
    bus_times = [int(bus) for bus in valid_buses(lines[1])]
    print(bus_times)
    print("solution1 = ", solution1(start_time, bus_times))

    bus_times = lines[1]
    bus_offsets = offsets(bus_times.split(","))
    print("solution2 = ", solution2fast(0, bus_offsets))


def solution1(start_time, bus_times):
    t = start_time
    while True:
        for bus in bus_times:
            if t % bus == 0:
                return bus * (t - start_time)
        t += 1


def is_valid(t, bus_times):
    for bus, offset in bus_times.items():
        if (t + offset) % bus:
            return False
    return True


def find_valid(t, bus_times):
    return [bus for bus, offset in bus_times.items() if (t + offset) % bus == 0]


def solution2(start_time, bus_times):
    t = start_time
    largest = max(bus_times.keys())
    largest_offset = bus_times[largest]
    while (t + largest_offset) % largest:
        t += 1
    step = largest
    while not is_valid(t, bus_times):
        t += step
    return t


def solution2fast(start_time, bus_times):
    t = start_time
    step = 1
    while True:
        valid = find_valid(t, bus_times)
        if len(valid) == len(bus_times):
            return t
        if valid:
            new_step = reduce(lambda a, b: a*b, valid)
            step = max(step, new_step)
        t += step
    return t


if __name__ == "__main__":
    run()
