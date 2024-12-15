import unittest
from ROBDD import ROBDDNode, build_robdd, parse_boolean_function, visualize_robdd
class TestORBDDEquivalenceChecker(unittest.TestCase):
    def setUp(self):
        # This runs before each test case
        self.ordering = ["A", "B", "C"]

    def test_equivalent_functions_simple(self):
        # Test De Morgan's Law: NOT (A AND B) == NOT A OR NOT B
        expr1 = parse_boolean_function(["A", "B", "AND", "NOT"])  # NOT (A AND B)
        expr2 = parse_boolean_function(["A", "NOT", "B", "NOT", "OR"])  # NOT A OR NOT B

        robdd1 = build_robdd(expr1, self.ordering)
        robdd2 = build_robdd(expr2, self.ordering)

        self.assertTrue(robdd1 == robdd2, "NOT (A AND B) should be equivalent to NOT A OR NOT B")

    def test_non_equivalent_functions(self):
        # Test (A AND B) != (A OR B)
        expr1 = parse_boolean_function(["A", "B", "AND"])  # A AND B
        expr2 = parse_boolean_function(["A", "B", "OR"])   # A OR B

        robdd1 = build_robdd(expr1, self.ordering)
        robdd2 = build_robdd(expr2, self.ordering)

        self.assertFalse(robdd1 == robdd2, "A AND B should not be equivalent to A OR B")

    def test_equivalent_functions_nested(self):
        # Test nested equivalence: (A AND B) OR C == C OR (A AND B)
        expr1 = parse_boolean_function(["A", "B", "AND", "C", "OR"])  # (A AND B) OR C
        expr2 = parse_boolean_function(["C", "A", "B", "AND", "OR"])  # C OR (A AND B)

        robdd1 = build_robdd(expr1, self.ordering)
        robdd2 = build_robdd(expr2, self.ordering)

        self.assertTrue(robdd1 == robdd2, "(A AND B) OR C should be equivalent to C OR (A AND B)")

    def test_non_equivalent_functions_complex(self):
        # Test complex non-equivalence: (A XOR B) XOR C == A XOR (B XOR C)
        expr1 = ('XOR', ('XOR', 'A', 'B'), 'C')  # (A XOR B) XOR C
        expr2 = ('XOR', 'A', ('XOR', 'B', 'C'))  # A XOR (B XOR C)
        robdd1 = build_robdd(expr1, self.ordering)
        robdd2 = build_robdd(expr2, self.ordering)

        self.assertTrue(robdd1 == robdd2, "(A XOR B) XOR C should not be equivalent to A XOR (B XOR C)")

    def test_tautology_vs_boolean_function(self):
        # Test tautology: A OR B != 1
        expr1 = parse_boolean_function(["A", "B", "OR"])  # A OR B
        expr2 = parse_boolean_function(["1"])            # Constant 1

        robdd1 = build_robdd(expr1, self.ordering)
        robdd2 = build_robdd(expr2, self.ordering)

        self.assertFalse(robdd1 == robdd2, "A OR B should not be equivalent to 1")
        
    def test_extra1(self):
        # Test : A AND (B OR C) == (A AND B) OR (A AND C)
        expr1 = ("AND", "A", ("OR", "B", "C"))
        expr2 = ("OR", ("AND", "A", "B"), ("AND", "A", "C"))

        robdd1 = build_robdd(expr1, self.ordering)
        robdd2 = build_robdd(expr2, self.ordering)

        self.assertTrue(robdd1 == robdd2, "A AND (B OR C) should be equivalent to (A AND B) OR (A AND C)")

    def test_extra2(self):
        # Test : A OR (B AND C) == (A OR B) AND (A OR C)
        expr1 = ("OR", "A", ("AND", "B", "C"))
        expr2 = ("AND", ("OR", "A", "B"), ("OR", "A", "C"))

        robdd1 = build_robdd(expr1, self.ordering)
        robdd2 = build_robdd(expr2, self.ordering)

        self.assertTrue(robdd1 == robdd2, "A OR (B AND C) should be equivalent to (A OR B) AND (A OR C)")

    def test_extra3(self):
        # Test : (A OR B OR C) AND (-A OR -B OR -C) != A OR (B AND C)
        expr1 = ("AND", ("OR", "C", ("OR", "A", "B")), ("OR", ("NOT", "C"), ("OR", ("NOT", "A"), ("NOT", "B"))))
        expr2 = ("OR", "A", ("AND", "B", "C"))

        robdd1 = build_robdd(expr1, self.ordering)
        robdd2 = build_robdd(expr2, self.ordering)

        self.assertFalse(robdd1 == robdd2, "(A OR B OR C) AND (-A OR -B OR -C) should not be equivalent to A OR (B AND C)")

if __name__ == "__main__":
    unittest.main()