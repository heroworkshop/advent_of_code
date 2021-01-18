from aocd_tools import load_input_data

EXAMPLE = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""".strip()


def run():
    input_data = load_input_data(2020, 4)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")

    passports = input_data.split("\n\n")
    print(passports)
    print("found {} passports".format(len(passports)))

    print("solution 1 = ", solution1(passports))
    print("solution 2 = ", solution2(passports))


def solution1(passports):
    passports = [interpret_passport(p) for p in passports]
    valid = [p for p in passports if validate(p)]

    return len(valid)


def interpret_passport(passport):
    passport = passport.replace("\n", " ")
    fields = passport.split(" ")
    d = {}
    for f in fields:
        a, _, b = f.partition(":")
        d[a] = b
    return d


def validate(passport):
    print(passport)
    required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for r in required:
        if r not in passport:
            print("missing ", r)
            return False

    return True


def validate_detailed(passport):
    print(passport)
    if not validate(passport):
        return False

    for k, v in passport.items():
        if not globals()[k](v):
            print("Invalid ", k)
            return False

    return True


def byr(v):
    try:
        v = int(v)
    except ValueError:
        return False
    return 1920 <= v <= 2002


def iyr(v):
    try:
        v = int(v)
    except ValueError:
        return False
    return 2010 <= v <= 2020


def eyr(v):
    try:
        v = int(v)
    except ValueError:
        return False
    return 2020 <= v <= 2030


def hgt(v):
    i, unit, _ = v.partition("in")
    lim_lower = 59
    lim_higher = 76
    if not unit:
        i, unit, _ = v.partition("cm")
        lim_lower = 150
        lim_higher = 193
    if not unit:
        return False
    try:
        i = int(i)
    except ValueError:
        return False
    return lim_lower <= i <= lim_higher


def hcl(v):
    _, _, v = v.partition("#")
    if len(v) != 6:
        return False
    for ch in v:
        if ch not in "1234567890abcdef":
            return False
    return True


def ecl(v):
    return v in "amb blu brn gry grn hzl oth".split(" ")


def pid(v):
    if len(v) != 9:
        return False
    for ch in v:
        if ch not in "1234567890":
            return False
    return True


def cid(v):
    return True


def solution2(passports):
    passports = [interpret_passport(p) for p in passports]
    valid = [p for p in passports if validate_detailed(p)]

    return len(valid)


if __name__ == "__main__":
    run()
