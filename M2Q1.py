
"""
M2Q1
June 4 2024
"""

import re

class BaseConverter:
    baseMap = {}
    for i in range(10):
        baseMap[str(i)] = i
    for i in range(10, 37):
        baseMap[chr(55 + i)] = i
    reverseMap = {}
    for k, v in baseMap.items():
        reverseMap[v] = k

    '''
    Convert a number in a given base to decimal
    number: str, number in the given base in string form
    base: int, base of the number
    '''
    def toDecimal(self, number, base):
        base_10 = 0
        for i, digit in enumerate(reversed(number)):
            currValue = self.baseMap[digit]
            base_10 += currValue * (base ** i)
        return base_10

    def from_decimal(self, number, base):
        digits = []
        while number > 0:
            number, remainder = divmod(number, base)
            digits.append(self.reverseMap[remainder])
        return ''.join(reversed(digits))

    def convert(self, number, from_base, to_base):
        decimal = self.toDecimal(number, from_base)
        return self.from_decimal(decimal, to_base)

    def represent(self, number, base):
        return f"0{self.reverseMap[base]}_{number}"

    def convert_bases(self, number):
        match = re.match(r'0([0-9A-Z])_(\w+)', number)
        from_base = self.baseMap[match.group(1)]
        number = match.group(2)
        to_base = self.baseMap['Q']
        converted_number = self.convert(number, from_base, to_base)
        return self.represent(converted_number, to_base)
    

# Main code

import unittest

class TestBaseConverter(unittest.TestCase):
    def setUp(self):
        self.converter = BaseConverter()

    def test_toDecimal(self):
        self.assertEqual(self.converter.toDecimal('100100', 2), 36)
        self.assertEqual(self.converter.toDecimal('44', 8), 36)
        self.assertEqual(self.converter.toDecimal('36', 10), 36)
        self.assertEqual(self.converter.toDecimal('24', 16), 36)
        self.assertEqual(self.converter.toDecimal('13', 33), 36)
        self.assertEqual(self.converter.toDecimal('12', 34), 36)
        self.assertEqual(self.converter.toDecimal('11', 35), 36)
        print("test_toDecimal passed")

    def test_decimal_36(self):
        self.assertEqual(self.converter.from_decimal(36, 2), '100100')
        self.assertEqual(self.converter.from_decimal(36, 8), '44')
        self.assertEqual(self.converter.from_decimal(36, 10), '36')
        self.assertEqual(self.converter.from_decimal(36, 16), '24')
        self.assertEqual(self.converter.from_decimal(36, 33), '13')
        self.assertEqual(self.converter.from_decimal(36, 34), '12')
        self.assertEqual(self.converter.from_decimal(36, 35), '11')
        print("test_decimal_36 passed")


    def test_decimal_123(self):
        self.assertEqual(self.converter.from_decimal(123, 2), '1111011')
        self.assertEqual(self.converter.from_decimal(123, 8), '173')
        self.assertEqual(self.converter.from_decimal(123, 16), '7B')
        self.assertEqual(self.converter.from_decimal(123, 26), '4J')
        self.assertEqual(self.converter.from_decimal(123, 33), '3O')
        self.assertEqual(self.converter.from_decimal(123, 35), '3I')
        print("test_decimal_123 passed")
        

if __name__ == '__main__':
    unittest.main()

