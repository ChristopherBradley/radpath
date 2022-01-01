import unittest
from euler_path import euler_path

class Test_euler_path(unittest.TestCase):

    def test_backtrack(self):
        """Ensure the system can backtrack to cover every node"""
        edges = [[(0,1),(0,2)], [(0,0),(0,1)]]
        double_edges = [[(0,0),(0,1)]]
        path = euler_path(edges, double_edges)
        assert path == [((0,1),(0,0)), ((0,0), (0,1)), ((0,1),(0,2))], path

    def test_direction(self):
        """Ensure the path goes in a straight line"""
        edges = [[(0,0),(0,1)], [(0,1), (0,10)], [(0,1), (1,1)]]
        double_edges = [[(0,0),(0,1)], [(0,1), (0,10)], [(0,1), (1,1)]]
        path = euler_path(edges, double_edges)
        assert path == [((0,0),(0,1)), ((0,1), (0,10)), ((0,10), (0,1)), ((0,1), (1,1)), ((1,1), (0,1)), ((0,1), (0,0))], path

if __name__ == '__main__':
    unittest.main()