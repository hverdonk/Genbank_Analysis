import unittest
import helper_functions as hf
from Bio.SeqFeature import FeatureLocation, CompoundLocation


class TestHelperFunctions(unittest.TestCase):
    def test_is_compound_location(self):
        f1 = FeatureLocation(10, 40, strand=+1)
        f2 = FeatureLocation(50, 59, strand=+1)
        f = CompoundLocation([f1, f2])
        self.assertTrue(hf.is_compound_location(f))
        self.assertFalse(hf.is_compound_location(f1))


if __name__ == '__main__':
    unittest.main()
