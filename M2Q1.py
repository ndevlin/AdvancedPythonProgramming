
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
    Convert a number in a given base to decimal numeric form
    numberIn: str, number in the given base in string form with prefix
    return: int, decimal numeric form of the number
    '''
    def toDecimal(self, numberIn):
        number, base = self.parseRepresentation(numberIn)
        decimal = 0
        for i, digit in enumerate(reversed(number)):
            currValue = self.baseMap[digit]
            decimal += currValue * (base ** i)
        return decimal

    '''
    Convert a decimal number to a given base
    numberIn: int, decimal numeric number
    toBase: int, base to convert to
    return: str, number in the new base in string form with prefix
    '''
    def fromDecimal(self, numberIn, toBase):
        digits = []
        number = numberIn
        while number > 0:
            number, remainder = divmod(number, toBase)
            digits.append(self.reverseMap[remainder])
        digits = reversed(digits)
        result = ''.join(digits)
        return self.represent(result, toBase)

    '''
    Convert a number from one base to another
    numberIn: str, number in its own base in string form with prefix
    toBase: int, base to convert to
    return: str, number in the new base in string form
    '''
    def convert(self, numberIn, toBase):
        decimal = self.toDecimal(numberIn)
        newVersion = self.fromDecimal(decimal, toBase)
        return newVersion

    '''
    Create a string representation of a number indicating its base
    Base indicators are represented as "0", base character, "_", e.g. "02_", "03_", ..., "0A_", "0B_", ...
    number: str, number in its own base in string form, without prefixed base indicator
    base: int, base of the number
    return: str, base-prefixed string representation of the number
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
    return: tuple of (str, int), number in string form and its base in decimal numeric form
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
        self.assertEqual(self.converter.convert('02_100100', 16), '0G_24')
        self.assertEqual(self.converter.convert('08_44', 10), '0A_36')
        self.assertEqual(self.converter.convert('0A_36', 2), '02_100100')
        self.assertEqual(self.converter.convert('0G_24', 8), '08_44')
        self.assertEqual(self.converter.convert('0X_13', 35), '0Z_11')
        self.assertEqual(self.converter.convert('0Y_12', 35), '0Z_11')
        self.assertEqual(self.converter.convert('0Z_11', 2), '02_100100')
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
        self.assertEqual(self.converter.toDecimal('02_100100'), 36)
        self.assertEqual(self.converter.toDecimal('08_44'), 36)
        self.assertEqual(self.converter.toDecimal('0A_36'), 36)
        self.assertEqual(self.converter.toDecimal('0G_24'), 36)
        self.assertEqual(self.converter.toDecimal('0X_13'), 36)
        self.assertEqual(self.converter.toDecimal('0Y_12'), 36)
        self.assertEqual(self.converter.toDecimal('0Z_11'), 36)
        print('\n', "test_toDecimal passed")

    def test_decimal_36(self):
        self.assertEqual(self.converter.fromDecimal(36, 2), '02_100100')
        self.assertEqual(self.converter.fromDecimal(36, 8), '08_44')
        self.assertEqual(self.converter.fromDecimal(36, 10), '0A_36')
        self.assertEqual(self.converter.fromDecimal(36, 16), '0G_24')
        self.assertEqual(self.converter.fromDecimal(36, 33), '0X_13')
        self.assertEqual(self.converter.fromDecimal(36, 34), '0Y_12')
        self.assertEqual(self.converter.fromDecimal(36, 35), '0Z_11')
        print('\n', "test_decimal_36 passed")

    def test_decimal_123(self):
        self.assertEqual(self.converter.fromDecimal(123, 2), '02_1111011')
        self.assertEqual(self.converter.fromDecimal(123, 8), '08_173')
        self.assertEqual(self.converter.fromDecimal(123, 16), '0G_7B')
        self.assertEqual(self.converter.fromDecimal(123, 26), '0Q_4J')
        self.assertEqual(self.converter.fromDecimal(123, 33), '0X_3O')
        self.assertEqual(self.converter.fromDecimal(123, 35), '0Z_3I')
        print('\n', "test_decimal_123 passed")
        
# Run tests
if __name__ == '__main__':
    unittest.main()

