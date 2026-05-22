import unittest
import random
import math

from iteration1_base import estimate_pi
from iteration2_threads import estimate_pi_threads
from iteration3_processes import estimate_pi_processes


class TestEstimatePi(unittest.TestCase):

    def setUp(self):
        random.seed(42)

    def test_range_sequential(self):
        pi_approx = estimate_pi(n_points=100000)
        self.assertGreater(pi_approx, 3.0)
        self.assertLess(pi_approx, 3.2)

    def test_range_threads(self):
        pi_approx = estimate_pi_threads(n_points=100000, n_jobs=4)
        self.assertGreater(pi_approx, 3.0)
        self.assertLess(pi_approx, 3.2)

    def test_range_processes(self):
        pi_approx = estimate_pi_processes(n_points=100000, n_jobs=4)
        self.assertGreater(pi_approx, 3.0)
        self.assertLess(pi_approx, 3.2)

    def test_accuracy_sequential(self):
        pi_approx = estimate_pi(n_points=1_000_000)
        error_percent = abs(pi_approx - math.pi) / math.pi * 100
        self.assertLess(error_percent, 1.0)

    def test_accuracy_threads(self):
        pi_approx = estimate_pi_threads(n_points=1_000_000, n_jobs=4)
        error_percent = abs(pi_approx - math.pi) / math.pi * 100
        self.assertLess(error_percent, 1.0)

    def test_accuracy_processes(self):
        pi_approx = estimate_pi_processes(n_points=1_000_000, n_jobs=4)
        error_percent = abs(pi_approx - math.pi) / math.pi * 100
        self.assertLess(error_percent, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)