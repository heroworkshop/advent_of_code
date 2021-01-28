from contextlib import suppress

# Generator A starts with 699
# Generator B starts with 124

A = 699
B = 124

FACTOR_A = 16807
FACTOR_B = 48271


def run():
    # print("solution1 = ", solution(40000000, Generator, Generator))
    print("solution2 = ", solution(5000000, Generator4, Generator8))


class Generator:
    DIVISOR = 2147483647

    def __init__(self, initial_value, factor):
        self.value = initial_value
        self.factor = factor

    def generate(self):
        self.value = (self.value * self.factor) % self.DIVISOR
        return self.value


class Generator4(Generator):
    def generate(self):
        while True:
            self.value = super().generate()
            if self.value % 4 == 0:
                return self.value


class Generator8(Generator):
    def generate(self):
        while True:
            self.value = super().generate()
            if self.value % 8 == 0:
                return self.value


def solution(rep_count, generator_type_a, generator_type_b):
    gen_a = generator_type_a(A, FACTOR_A)
    gen_b = generator_type_b(B, FACTOR_B)
    count = 0
    for i in range(rep_count):
        # print(f"{a:>12} {b:>12}")
        with suppress(ZeroDivisionError):
            if i % (rep_count // 100) == 0:
                print(".", end="")
        a = gen_a.generate()
        b = gen_b.generate()
        if compare_loword(a, b):
            count += 1
    print()
    return count


def compare_loword(a, b):
    return (a & 0xffff) == (b & 0xffff)



if __name__ == "__main__":
    run()
