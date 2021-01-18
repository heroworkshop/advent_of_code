from collections import namedtuple

from aocd_tools import load_input_data

EXAMPLE = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""".strip()

EXAMPLE2 = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""".strip()


Rule = namedtuple("rule", "id value")


def parse(line):
    return line.split("\n")


def int_list(s):
    return [int(v) for v in s.split(" ")]


def parse_rule(line):
    rule_id_str, _, rhs = line.partition(":")
    rule_id = int(rule_id_str)
    rhs = rhs.strip()
    if rhs.startswith('"'):
        value = rhs[1]
    else:
        value = [int_list(opt.strip()) for opt in rhs.split("|")]
    return Rule(rule_id, value)


def run():
    input_data = load_input_data(2020, 19)
    # input_data = EXAMPLE2
    print(f"loaded input data ({len(input_data)} bytes)")
    rules, messages = [parse(part) for part in input_data.split("\n\n")]
    rules = [parse_rule(line) for line in rules]
    rules = {r.id: r.value for r in rules}
    print("solution1 = ", solution1(rules, messages))
    print("solution2 = ", solution2(rules, messages))


def matches_rule(rules, n, message):
    rule = rules[n]
    if isinstance(rule, str):
        if message == "":
            return False, message
        if message[0] == rule:
            return True, message[1:]
        else:
            return False, message
    for opt in rule:
        remainder = message
        ok = True
        for part in opt:
            m, remainder = matches_rule(rules, part, remainder)
            if not m:
                ok = False
                break
        if ok:
            return True, remainder
    return False, message


def is_valid(rules, message):
    valid, remainder = matches_rule(rules, 0, message)
    return valid and remainder == ""


def is_valid2(rules, message):
    count42 = 0
    while message:
        valid, remainder = matches_rule(rules, 42, message)
        if valid:
            message = remainder
            count42 += 1
        else:
            break
    if count42 < 2:
        return False
    count31 = 0
    while message:
        valid, remainder = matches_rule(rules, 31, message)
        if valid:
            message = remainder
            count31 += 1
        else:
            break
    if count31 < 1 or count31 > count42 - 1:
        return False
    return message == ""


def solution1(rules, messages):
    print(rules)
    valid_messages = [message for message in messages if is_valid(rules, message)]
    print(valid_messages)
    return len(valid_messages)


def solution2(rules, messages):
    # 0: 8 11
    # 0: 42 42 31
    # 42 42 31   = 2, 1
    # 42 42 42 31= 3, 1
    # 42 42 42 31 31 = 3, 2
    # 42 42 42 42 42 31 31 31 = 5, 3
    # extra_rules = """8: 42 | 42 8
    # 11: 42 31 | 42 11 31""".split("\n")
    # for line in extra_rules:
    #     rule = parse_rule(line)
    #     rules[rule.id] = rule.value
    valid_messages = [message for message in messages if is_valid2(rules, message)]
    print(valid_messages)
    return len(valid_messages)


if __name__ == "__main__":
    run()
