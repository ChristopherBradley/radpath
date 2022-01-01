import unittest
from double_edges import choose_double_edges

class Test_double_edges(unittest.TestCase):

    def test_kite(self):
        edges = [[(244, 313), (309, 421)], [(309, 421), (420, 359)], [(420, 359), (244, 313)], [(244, 313), (350, 237)],
                 [(350, 237), (420, 359)], [(350, 237), (557, 134)]]
        double_edges = choose_double_edges(edges)
        # Should probably make the assertion allow the edges to be flipped too.
        assert double_edges == [((244, 313), (420, 359)), ((350, 237), (557, 134))], double_edges

if __name__ == '__main__':
    unittest.main()