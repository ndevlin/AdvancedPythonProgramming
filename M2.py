
"""
M2
June 6 2024
"""


"""
Note: 
It seems like baseZ should be considered base 35, rather than base 36.
There would need to be some additional letter between H=17 and Z otherwise.
It seems it should be 
A 10, B 11, C 12, D 13, E 14, F 15, G 16, H 17, I 18, J 19, K 20, L 21, M 22, 
N 23, O 24, P 25, Q 26, R 27, S 28, T 29, U 30, V 31, W 32, X 33, Y 34, Z 35
It seems that some of the test case examples given in the prompt towards the ends 
are are off by one because of this. 
However, I have included the ability to use a Base "[", i.e. Base36, which is the next 
char after "Z" in the Ascii table, as base 36 in case we wanted that.
"""

import re
import unittest

class BaseConverter:
    characterBaseToDecimalMap = {}
    decimalBaseToCharMap = {}

    def __init__(self):
        for i in range(10):
            self.characterBaseToDecimalMap[str(i)] = i
        for i in range(10, 37):
            # Start with A at 10 since Ascii 65 is A
            self.characterBaseToDecimalMap[chr(55 + i)] = i
        for k, v in self.characterBaseToDecimalMap.items():
            self.decimalBaseToCharMap[v] = k
    

    '''
    Converts an input base to its decimal numeric form
    base: str or int, base to convert
    return: int, decimal numeric form of the base
    '''
    def getBaseInDecimal(self, base):
        if isinstance(base, str):
            return self.characterBaseToDecimalMap[base]
        else:
            return base

    '''
    Convert a number in a given base to decimal numeric form
    numberIn: str, number in the given base in string form with prefix
    return: int, decimal numeric form of the number
    '''
    def toDecimal(self, numberIn):
        number, base = self.parseRepresentation(numberIn)
        decimal = 0
        for i, digit in enumerate(reversed(number)):
            currValue = self.characterBaseToDecimalMap[digit]
            decimal += currValue * (base ** i)
        return decimal

    '''
    Convert a decimal number to a given base
    numberIn: int, decimal numeric number
    toBase: int or string, base to convert to
    return: str, number in the new base in string form with prefix
    '''
    def fromDecimal(self, numberIn, toBase):
        toBase = self.getBaseInDecimal(toBase)
        digits = []
        number = numberIn
        while number > 0:
            number, remainder = divmod(number, toBase)
            digits.append(self.decimalBaseToCharMap[remainder])
        digits = reversed(digits)
        result = ''.join(digits)
        return self.represent(result, toBase)

    '''
    Convert a number from one base to another
    numberIn: str, number in its own base in string form with prefix
    toBase: int or string, base to convert to
    return: str, number in the new base in string form
    '''
    def convert(self, numberIn, toBase):
        toBase = self.getBaseInDecimal(toBase)
        decimal = self.toDecimal(numberIn)
        newVersion = self.fromDecimal(decimal, toBase)
        return newVersion

    '''
    Create a string representation of a number indicating its base
    Base indicators are represented as "0", base character, "_", e.g. "02_", "03_", ..., "0A_", "0B_", ...
    number: str, number in its own base in string form, without prefixed base indicator
    base: int or string, base of the number
    return: str, base-prefixed string representation of the number
    '''
    def represent(self, number, base):
        base = self.getBaseInDecimal(base)
        result = "0" + self.decimalBaseToCharMap[base] + "_" + number
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
        base = self.characterBaseToDecimalMap[baseChar[1]]    # Skip the 0
        return number, base


'''
# Base Converter Testing code
class TestBaseConverter(unittest.TestCase):
    def setUp(self):
        self.converter = BaseConverter()

    def test_getBaseInDecimal(self):
        self.assertEqual(self.converter.getBaseInDecimal('2'), 2)
        self.assertEqual(self.converter.getBaseInDecimal('8'), 8)
        self.assertEqual(self.converter.getBaseInDecimal('A'), 10)
        self.assertEqual(self.converter.getBaseInDecimal('G'), 16)
        self.assertEqual(self.converter.getBaseInDecimal('O'), 24)
        self.assertEqual(self.converter.getBaseInDecimal('P'), 25)
        self.assertEqual(self.converter.getBaseInDecimal(2), 2)
        self.assertEqual(self.converter.getBaseInDecimal(8), 8)
        self.assertEqual(self.converter.getBaseInDecimal(10), 10)
        self.assertEqual(self.converter.getBaseInDecimal(16), 16)
        self.assertEqual(self.converter.getBaseInDecimal(24), 24)
        self.assertEqual(self.converter.getBaseInDecimal(25), 25)
        print('\n', "test_getBaseInDecimal passed")

    def test_parseRepresentation(self):
        self.assertEqual(self.converter.parseRepresentation('02_100100'), ('100100', 2))
        self.assertEqual(self.converter.parseRepresentation('08_44'), ('44', 8))
        self.assertEqual(self.converter.parseRepresentation('0A_36'), ('36', 10))
        self.assertEqual(self.converter.parseRepresentation('0G_24'), ('24', 16))
        self.assertEqual(self.converter.parseRepresentation('0O_13'), ('13', 24))
        self.assertEqual(self.converter.parseRepresentation('0P_12'), ('12', 25))
        print('\n', "test_parseRepresentation passed")

    def test_convert(self):
        self.assertEqual(self.converter.convert('02_100100', "G"), '0G_24')
        self.assertEqual(self.converter.convert('08_44', 10), '0A_36')
        self.assertEqual(self.converter.convert('0A_36', 2), '02_100100')
        self.assertEqual(self.converter.convert('0G_24', 8), '08_44')
        self.assertEqual(self.converter.convert('0X_13', "Z"), '0Z_11')
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

# Main Q1
if __name__ == '__main__':

    converter = BaseConverter()

    numbers = [36, 123, 456]

    bases = [2, 8, 16]

    for number in numbers:
        print(f"\nTesting number {number}:")

        currNumber = converter.represent(str(number), 10)

        # Convert the number to each base
        for base in bases:
            print(f"\nConverting {currNumber} to base {base}:")
            numInBase = converter.convert(currNumber, base)
            print(f"Number {currNumber} in base {base} is {numInBase}")
            currNumber = numInBase

        print(f"\nConverting {currNumber} back to base 10:")
        numInDecimal = converter.toDecimal(currNumber)
        print(f"Number {currNumber} is {numInDecimal} in decimal")

        # Check if the number is the same after converting back to base 10
        if numInDecimal == number:
            print(f"Success: {numInDecimal} == {numInDecimal}")
        else:
            print(f"Failure: {numInDecimal} != {numInDecimal}")

    # Run the unit tests
    unittest.main()
'''


"""
2
"""


