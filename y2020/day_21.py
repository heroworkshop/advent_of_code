from collections import defaultdict

from aocd_tools import load_input_data

EXAMPLE = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".strip()

def parse(line):
    ingredients_str, _, allergens_str = line.partition("(contains")
    ingredients = ingredients_str.strip().split()
    allergens = [a.strip() for a in allergens_str[:-1].strip().split(",")]
    return ingredients, allergens


def run():
    input_data = load_input_data(2020, 21)
    # input_data = EXAMPLE
    print(f"loaded input data ({len(input_data)} bytes)")
    lines = [parse(line) for line in input_data.split("\n")]
    count, solved = solution1(lines)
    print("solution1 = ", count)
    print("solution2 = ", solution2(solved))


def solution1(lines):
    ingredient_tally = defaultdict(int)
    allergen_suspects = defaultdict(list)
    solved = dict()

    for ingredients, allergens in lines:
        for i in ingredients:
            ingredient_tally[i] += 1
        for a in allergens:
            allergen_suspects[a].append(ingredients)

    merged_suspects = {a: set(ingredient_tally.keys()) for a in allergen_suspects}
    for allergen, suspects in allergen_suspects.items():
        for sub_list in suspects:
            merged_suspects[allergen] = merged_suspects[allergen].intersection(set(sub_list))

    while len(solved) < len(merged_suspects):
        print(merged_suspects)
        eurekas = [a for a, suspects in merged_suspects.items() if len(suspects) == 1]
        if not eurekas:
            raise RuntimeError("Cannot resolve allergens")
        for allergen in eurekas:
            solved[allergen] = merged_suspects[allergen].pop()
            # ingredients cannot contain more than one allergen so remove from other allergens
            for suspects in merged_suspects.values():
                suspects.discard(solved[allergen])

    print(solved)
    counts = [count for ingredient, count in ingredient_tally.items()
              if ingredient not in solved.values()]
    return sum(counts), solved


def solution2(solved):
    ingredients = [solved[allergen] for allergen in sorted(solved.keys())]

    return ",".join(ingredients)


if __name__ == "__main__":
    run()
