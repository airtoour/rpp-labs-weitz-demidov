import unittest
from triangle_func import get_triangle_type, IncorrectTriangleSides

class TestGetTriangleType(unittest.TestCase):
    def test_equilateral_triangle(self):
        self.assertEqual(get_triangle_type(3, 3, 3), "equilateral")

    def test_isosceles_triangle(self):
        self.assertEqual(get_triangle_type(5, 5, 6), "isosceles")

    def test_nonequilateral_triangle(self):
        self.assertEqual(get_triangle_type(5, 6, 7), "nonequilateral")

    def test_incorrect_triangle_sides(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(20, 2, 2)


if __name__ == '__main__':
    unittest.main()