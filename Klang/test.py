""" Klang Testing """
import unittest
import random
from klang import klang


class TestKlang(unittest.TestCase):
    """ Klang Test Cases """

    def test_error(self):
        """ Test Errors """

        res, err = klang.run('<stdin>', "123 123 123")
        self.assertEqual(res, None)
        self.assertNotEqual(err, None)

        # !Error: Division by Zero
        int1, int2 = 0, 0
        res, err = klang.run('<stdin>', f"{int1} / {int2}")
        self.assertEqual(res, None)
        self.assertNotEqual(err, None)

        res, err = klang.run('<stdin>', "=")
        self.assertEqual(res, None)
        self.assertNotEqual(err, None)

        res, err = klang.run('<stdin>', "IF")
        self.assertEqual(res, None)
        self.assertNotEqual(err, None)

        res, err = klang.run('<stdin>', "b")
        self.assertEqual(res, None)
        self.assertNotEqual(err, None)

        res, err = klang.run('<stdin>', "!")
        self.assertEqual(res, None)
        self.assertNotEqual(err, None)

        res, err = klang.run('<stdin>', "NOT 2")
        self.assertEqual(res, None)
        self.assertNotEqual(err, None)

        res, err = klang.run('<stdin>', "IF a = 1 THEN 123")
        self.assertEqual(res, None)
        self.assertNotEqual(err, None)

        res, err = klang.run('<stdin>', "IF a == 1")
        self.assertEqual(res, None)
        self.assertNotEqual(err, None)

        res, err = klang.run('<stdin>', "FUN test(a) => a / 0")
        self.assertEqual(str(res), "<function test>")
        self.assertEqual(err, None)
        res, err = klang.run('<stdin>', "test(10)")
        self.assertEqual(res, None)
        self.assertNotEqual(err, None)

    def test_number(self):
        """ Test Raw Number Input """

        for i in range(-100, 100):
            res, err = klang.run('<stdin>', str(i))
            self.assertEqual(res.value, i)
            self.assertEqual(err, None)

    def test_math_op(self):
        """ Test Math Operation """

        # Addition
        for __ in range(100):
            int1 = random.randint(-100, 100)
            int2 = random.randint(-100, 100)

            res, err = klang.run('<stdin>', f"{int1} + {int2}")
            self.assertEqual(res.value, int1 + int2)
            self.assertEqual(err, None)

            float1 = random.random() * 1000
            float2 = random.random() * 1000

            res, err = klang.run('<stdin>', f"{float1} + {float2}")
            self.assertEqual(res.value, float1 + float2)
            self.assertEqual(err, None)

        # Subtraction
        for __ in range(100):
            int1 = random.randint(-100, 100)
            int2 = random.randint(-100, 100)

            res, err = klang.run('<stdin>', f"{int1} - {int2}")
            self.assertEqual(res.value, int1 - int2)
            self.assertEqual(err, None)

            float1 = random.random() * 1000
            float2 = random.random() * 1000
            res, err = klang.run('<stdin>', f"{float1} - {float2}")
            self.assertEqual(res.value, float1 - float2)
            self.assertEqual(err, None)

        # Multiplication
        for __ in range(100):
            int1 = random.randint(-100, 100)
            int2 = random.randint(-100, 100)

            res, err = klang.run('<stdin>', f"{int1} * {int2}")
            self.assertEqual(res.value, int1 * int2)
            self.assertEqual(err, None)

            float1 = random.random() * 1000
            float2 = random.random() * 1000
            res, err = klang.run('<stdin>', f"{float1} * {float2}")
            self.assertEqual(res.value, float1 * float2)
            self.assertEqual(err, None)

        # Division
        for __ in range(100):
            int1 = random.randint(-100, 100)
            int2 = random.choice((random.randint(-100,
                                                 -1), random.randint(1, 100)))

            res, err = klang.run('<stdin>', f"{int1} / {int2}")
            self.assertEqual(res.value, int1 / int2)
            self.assertEqual(err, None)

            float1 = random.random() * 1000
            float2 = random.random() * 1000
            res, err = klang.run('<stdin>', f"{float1} / {float2}")
            self.assertEqual(res.value, float1 / float2)
            self.assertEqual(err, None)

        # Power
        for __ in range(100):
            int1 = random.randint(0, 10)
            int2 = random.randint(0, 10)

            res, err = klang.run('<stdin>', f"{int1} ^ {int2}")
            self.assertEqual(res.value, int1**int2)
            self.assertEqual(err, None)

            float1 = random.random() * 10
            float2 = random.random() * 10
            res, err = klang.run('<stdin>', f"{float1} ^ {float2}")
            self.assertEqual(res.value, float1**float2)
            self.assertEqual(err, None)

    def test_variables(self):
        """ Test Variable Assignment """

        for i in range(-100, 100):

            # Assignment
            res, err = klang.run('<stdin>', f"VAR a = {i}")
            self.assertEqual(res.value, i)
            self.assertEqual(err, None)

            # Access
            res, err = klang.run('<stdin>', "a")
            self.assertEqual(res.value, i)
            self.assertEqual(err, None)

            rand = i + random.randint(-100, 100)

            res, err = klang.run('<stdin>', f"a + {rand}")
            self.assertEqual(res.value, i + rand)
            self.assertEqual(err, None)

            # Reassignment
            res, err = klang.run('<stdin>', f"a = {rand}")
            self.assertEqual(res.value, rand)
            self.assertEqual(err, None)

    def test_logical_op(self):
        """ Test logical operations """

        for __ in range(100):
            int1 = random.randint(-10, 10)
            int2 = random.randint(-10, 10)

            res, err = klang.run('<stdin>', f"{int1} == {int2}")
            self.assertEqual(res.value, int1 == int2)
            self.assertEqual(err, None)

            res, err = klang.run('<stdin>', f"{int1} != {int2}")
            self.assertEqual(res.value, int1 != int2)
            self.assertEqual(err, None)

            res, err = klang.run('<stdin>', f"{int1} > {int2}")
            self.assertEqual(res.value, int1 > int2)
            self.assertEqual(err, None)

            res, err = klang.run('<stdin>', f"{int1} < {int2}")
            self.assertEqual(res.value, int1 < int2)
            self.assertEqual(err, None)

            res, err = klang.run('<stdin>', f"{int1} >= {int2}")
            self.assertEqual(res.value, int1 >= int2)
            self.assertEqual(err, None)

            res, err = klang.run('<stdin>', f"{int1} <= {int2}")
            self.assertEqual(res.value, int1 <= int2)
            self.assertEqual(err, None)

            res, err = klang.run('<stdin>', "NOT TRUE")
            self.assertEqual(res.value, 0)
            self.assertEqual(err, None)

            res, err = klang.run('<stdin>', "NOT FALSE")
            self.assertEqual(res.value, 1)
            self.assertEqual(err, None)

    def test_condition(self):
        """ Test Conditional Statements """

        res, err = klang.run('<stdin>', "IF TRUE THEN 123 ELSE 456")
        self.assertEqual(res.value, 123)
        self.assertEqual(err, None)

        res, err = klang.run('<stdin>', "IF FALSE THEN 123 ELSE 456")
        self.assertEqual(res.value, 456)
        self.assertEqual(err, None)

        res, err = klang.run(
            '<stdin>',
            "IF FALSE THEN 123 ELIF FALSE THEN 456 ELIF TRUE THEN 789 ELSE 100"
        )
        self.assertEqual(res.value, 789)
        self.assertEqual(err, None)

        res, err = klang.run('<stdin>', "IF 1 == 1 THEN 123 ELSE 456")
        self.assertEqual(res.value, 123)
        self.assertEqual(err, None)

        res, err = klang.run('<stdin>', "IF 1 != 1 THEN 123 ELSE 456")
        self.assertEqual(res.value, 456)
        self.assertEqual(err, None)

        res, err = klang.run('<stdin>', "VAR a = 1")
        res, err = klang.run('<stdin>', "IF a == 1 THEN 123 ELSE 456")
        self.assertEqual(res.value, 123)
        self.assertEqual(err, None)

        res, err = klang.run('<stdin>', "IF a != 1 THEN 123 ELSE 456")
        self.assertEqual(res.value, 456)
        self.assertEqual(err, None)

    def test_function(self):
        """ Test Function Definition & Call """

        res, err = klang.run('<stdin>', "FUN add(a, b) => a + b")
        self.assertEqual(str(res), '<function add>')
        self.assertEqual(err, None)

        res, err = klang.run('<stdin>', "add(5, 6)")
        self.assertEqual(res.value, 11)
        self.assertEqual(err, None)

        res, err = klang.run('<stdin>', "VAR a = FUN (a) => a / 10")
        self.assertEqual(str(res), '<function <anonymous>>')
        self.assertEqual(err, None)

        res, err = klang.run('<stdin>', "a(10)")
        self.assertEqual(res.value, 1)
        self.assertEqual(err, None)


if __name__ == '__main__':
    unittest.main()
