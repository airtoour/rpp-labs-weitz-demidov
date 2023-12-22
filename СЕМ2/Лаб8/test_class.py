from triangle_class import Triangle, IncorrectTriangleSides

def test_create_triangle():
    t = Triangle(5, 6, 7)
    assert t.a == 5
    assert t.b == 6
    assert t.c == 7

def test_triangle_type():
    t1 = Triangle(3, 3, 3)
    assert t1.triangle_type() == "equilateral"
    t2 = Triangle(5, 5, 6)
    assert t2.triangle_type() == "isosceles"
    t3 = Triangle(5, 6, 7)
    assert t3.triangle_type() == "nonequilateral"

def test_perimeter():
    t = Triangle(5, 6, 7)
    assert t.perimeter() == 18

def test_incorrect_triangle_sides():
    try:
        t = Triangle(0, 0, 0)
    except IncorrectTriangleSides as e:
        assert str(e) == "Incorrect Triangle Sides."


if __name__ == "__main__":
    test_create_triangle()
    test_triangle_type()
    test_perimeter()
    test_incorrect_triangle_sides()
