
"""
M2Q1
June 4 2024
"""

import re
import unittest

class BaseConverter:
    baseMap = {}
    for i in range(10):
        baseMap[str(i)] = i
    for i in range(10, 37):
        # Start with A at 10 since Ascii 65 is A
        baseMap[chr(55 + i)] = i
    reverseMap = {}
    for k, v in baseMap.items():
        reverseMap[v] = k

    '''
    Convert a number in a given base to decimal
    number: str, number in the given base in string form
    base: int, base of the number
    '''
    def toDecimal(self, numberIn, base):
        base_10 = 0
        for i, digit in enumerate(reversed(numberIn)):
            currValue = self.baseMap[digit]
            base_10 += currValue * (base ** i)
        return base_10

    '''
    Convert a decimal number to a given base
    numberIn: int, decimal number
    base: int, base to convert to
    '''
    def fromDecimal(self, numberIn, base):
        digits = []
        number = numberIn
        while number > 0:
            number, remainder = divmod(number, base)
            digits.append(self.reverseMap[remainder])
        digits = reversed(digits)
        result = ''.join(digits)
        return result

    '''
    Convert a number from one base to another
    number: str, number in its own base in string form
    fromBase: int, base of the incoming number
    toBase: int, base to convert to
    '''
    def convert(self, number, fromBase, toBase):
        decimal = self.toDecimal(number, fromBase)
        return self.fromDecimal(decimal, toBase)

    '''
    Create a string representation of a number indicating its base
    number: str, number in its own base in string form, without prepended base indicator
    base: int, base of the number
    '''
    def represent(self, number, base):
        result = "0" + self.reverseMap[base] + "_" + number
        return result
    
    '''
    The opposite of the represent function; 
    takes in a prefixed string e.g. 0A_36, 
    and returns the number in string form and its base in decimal numeric form
    as a tuple, e.g. ('36', 10)
    representation: str, base-prefixed string representation of the number
    '''
    def parseRepresentation(self, representation):
        baseChar, number = representation.split('_')
        base = self.baseMap[baseChar[1]]    # Skip the 0
        return number, base


# Testing code

class TestBaseConverter(unittest.TestCase):
    def setUp(self):
        self.converter = BaseConverter()

    def test_parseRepresentation(self):
        self.assertEqual(self.converter.parseRepresentation('02_100100'), ('100100', 2))
        self.assertEqual(self.converter.parseRepresentation('08_44'), ('44', 8))
        self.assertEqual(self.converter.parseRepresentation('0A_36'), ('36', 10))
        self.assertEqual(self.converter.parseRepresentation('0G_24'), ('24', 16))
        self.assertEqual(self.converter.parseRepresentation('0O_13'), ('13', 24))
        self.assertEqual(self.converter.parseRepresentation('0P_12'), ('12', 25))
        print('\n', "test_parseRepresentation passed")

    def test_convert(self):
        self.assertEqual(self.converter.convert('100100', 2, 16), '24')
        self.assertEqual(self.converter.convert('44', 8, 10), '36')
        self.assertEqual(self.converter.convert('36', 10, 2), '100100')
        self.assertEqual(self.converter.convert('24', 16, 8), '44')
        self.assertEqual(self.converter.convert('13', 33, 35), '11')
        self.assertEqual(self.converter.convert('12', 34, 35), '11')
        self.assertEqual(self.converter.convert('11', 35, 2), '100100')
        print('\n', "test_convert passed")

    def test_represent(self):
        self.assertEqual(self.converter.represent('100100', 2), '02_100100')
        self.assertEqual(self.converter.represent('44', 8), '08_44')
        self.assertEqual(self.converter.represent('36', 10), '0A_36')
        self.assertEqual(self.converter.represent('24', 16), '0G_24')
        self.assertEqual(self.converter.represent('12', 24), '0O_12')
        self.assertEqual(self.converter.represent('11', 25), '0P_11')
        self.assertEqual(self.converter.represent('10', 35), '0Z_10')
        print('\n', "test_represent passed")

    def test_toDecimal(self):
        self.assertEqual(self.converter.toDecimal('100100', 2), 36)
        self.assertEqual(self.converter.toDecimal('44', 8), 36)
        self.assertEqual(self.converter.toDecimal('36', 10), 36)
        self.assertEqual(self.converter.toDecimal('24', 16), 36)
        self.assertEqual(self.converter.toDecimal('13', 33), 36)
        self.assertEqual(self.converter.toDecimal('12', 34), 36)
        self.assertEqual(self.converter.toDecimal('11', 35), 36)
        print('\n', "test_toDecimal passed")

    def test_decimal_36(self):
        self.assertEqual(self.converter.fromDecimal(36, 2), '100100')
        self.assertEqual(self.converter.fromDecimal(36, 8), '44')
        self.assertEqual(self.converter.fromDecimal(36, 10), '36')
        self.assertEqual(self.converter.fromDecimal(36, 16), '24')
        self.assertEqual(self.converter.fromDecimal(36, 33), '13')
        self.assertEqual(self.converter.fromDecimal(36, 34), '12')
        self.assertEqual(self.converter.fromDecimal(36, 35), '11')
        print('\n', "test_decimal_36 passed")

    def test_decimal_123(self):
        self.assertEqual(self.converter.fromDecimal(123, 2), '1111011')
        self.assertEqual(self.converter.fromDecimal(123, 8), '173')
        self.assertEqual(self.converter.fromDecimal(123, 16), '7B')
        self.assertEqual(self.converter.fromDecimal(123, 26), '4J')
        self.assertEqual(self.converter.fromDecimal(123, 33), '3O')
        self.assertEqual(self.converter.fromDecimal(123, 35), '3I')
        print('\n', "test_decimal_123 passed")
        
# Run tests
if __name__ == '__main__':
    unittest.main()

