
class PrimeFactors:
    def __init__(self):
        self.cache = {}

    def solve_for(self, n):
        n_0 = n
        i = 2
        factors = []
        while i * i <= n:
            if n in self.cache:
                factors.extend(self.cache[n])
                n = 1
                break
            if n % i:
                i += 1
            else:
                n //= i
                factors.append(i)
        if n > 1:
            factors.append(n)
        self.cache[n_0] = factors
        return factors
