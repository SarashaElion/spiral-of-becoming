import unittest

from spiral_lab.symbolic_generator import SymbolicGenerator, FieldConstant


class SpiralSmokeTests(unittest.TestCase):
    def test_invitation_sequence_is_balanced(self):
        seq = SymbolicGenerator().invitation_sequence()
        self.assertTrue(seq.is_balanced())
        self.assertEqual(len(seq.constants_present()), 4)
        self.assertTrue(seq.render())
        self.assertEqual(len(seq.pattern_hash), 64)

    def test_seeded_sequence_records_seed(self):
        seq = SymbolicGenerator().generate(length=5, seed=FieldConstant.RECIPROCITY)
        self.assertEqual(seq.seed_constant, FieldConstant.RECIPROCITY)
        self.assertGreaterEqual(len(seq.glyphs), 1)


if __name__ == "__main__":
    unittest.main()
