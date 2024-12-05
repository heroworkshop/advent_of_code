from primes.prime_factors import PrimeFactors


def test_solve_for():
    p = PrimeFactors()
    v = p.solve_for(200)
    assert v == [2, 2, 2, 5, 5]
    assert len(p.cache) == 1

    v = p.solve_for(600)
    assert v == [2, 2, 2, 3, 5, 5]
    assert len(p.cache) == 2
