from aocd_tools import load_input_data

EXAMPLE = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"

EXAMPLE2 = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def parse(line):
    sig_patterns, outputs = line.split("|")
    return sig_patterns.split(), outputs.split()


def run():
    input_data = load_input_data()
    print(f"loaded input data ({len(input_data)} bytes)")
    # input_data = EXAMPLE2
    lines = [parse(line) for line in input_data.split("\n")]
    print("solution1 = ", solution1(lines))
    print("solution2 = ", solution2(lines))


def solution1(lines):
    count = 0
    for seg_patterns, outputs in lines:
        count += len([x for x in outputs if len(x) in (7, 4, 2, 3)])
    return count


def decode(line):
    seg_patterns, outputs = line
    seg_patterns = [set(s) for s in seg_patterns]
    solved = dict()
    simples = {7: 8, 2: 1, 3: 7, 4: 4}
    for sp in seg_patterns:
        if len(sp) in simples:
            solved[simples[len(sp)]] = sp

    for sp in seg_patterns:
        if len(sp) == 5:  # 5, 2, 3
            if len(sp.intersection(solved[4])) == 2:
                solved[2] = sp
            elif len(sp.intersection(solved[1])) == 2:
                solved[3] = sp
            else:
                solved[5] = sp
        if len(sp) == 6:  # 0, 9, 6
            if len(sp.intersection(solved[1])) == 1:
                solved[6] = sp
            elif len(sp.intersection(solved[4])) == 4:
                solved[9] = sp
            else:
                solved[0] = sp

    def mk_str_key(x):
        return "".join(sorted([a for a in x]))

    rev_solved = {mk_str_key(v): str(k) for k, v in solved.items()}

    number = [rev_solved[mk_str_key(op)] for op in outputs]
    return int("".join(number))


def solution2(lines):
    return sum(decode(line) for line in lines)


if __name__ == "__main__":
    run()
