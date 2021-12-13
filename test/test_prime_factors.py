import unittest
from primes.prime_factors import PrimeFactors

class TestPrimeFactors(unittest.TestCase):
    def test_solve_for(self):
        p = PrimeFactors()
        v = p.solve_for(200)
        self.assertEqual([2,2,2,5,5], v)
        self.assertEqual(1, len(p.cache))
        v = p.solve_for(600)
        self.assertEqual([2,2,2,3,5,5], v)
        self.assertEqual(2, len(p.cache))


if __name__ == '__main__':
    unittest.main()
