
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
        if number == 0:
            return self.represent("0", toBase)
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

# Calling the class BaseXNumber instead of BaseXDigit
class BaseXNumber:
    converter = BaseConverter()
    fullBaseXString = ""
    baseTypeInString = ""
    baseTypeInDecimal = 10
    numberInDecimal = 0
    numberInBaseString = ""
    numberInDecimalString = ""

    def __init__(self, input="0A_0"):
        if isinstance(input, BaseXNumber):
            input = input.getNumberInOriginalBase()
        elif isinstance(input, int):
            input = self.converter.fromDecimal(input, 10)
        if not type(input) == str:
            raise ValueError("Input must be a BaseXNumber, a string, or an int")
        self.fullBaseXString = input
        self.baseTypeInString = input[1]
        self.baseTypeInDecimal = self.converter.getBaseInDecimal(self.baseTypeInString)
        self.numberInBaseString = input[3:]
        self.numberInDecimal = self.converter.toDecimal(input)
        self.numberInDecimalString = self.converter.fromDecimal(self.numberInDecimal, 10)
    
    def __str__(self):
        return self.numberInDecimalString

    def __repr__(self):
        return self.numberInDecimalString
    
    def get(self):
        return self.numberInDecimalString
    
    def getNumberInOriginalBase(self):
        return self.fullBaseXString
    
    def getInNumericDecimal(self):
        return self.numberInDecimal

    # Allows adding, subtracting, multiplying, mod-ing with multiple types of data
    def convertOtherToDecimal(self, other):
        otherInDecimal = 0
        if isinstance(other, BaseXNumber):
            otherInDecimal = other.getInNumericDecimal()
        elif isinstance(other, int):
            otherInDecimal = other
        elif isinstance(other, str):
            otherInDecimal = self.converter.toDecimal(other)
        else:
            raise ValueError("Input must be a BaseXNumber, a string, or an integer")
        return otherInDecimal

    def __add__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return self.numberInDecimal + otherInDecimal
    
    def __radd__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return otherInDecimal + self.numberInDecimal

    def __sub__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return self.numberInDecimal - otherInDecimal
    
    def __rsub__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return otherInDecimal - self.numberInDecimal
    
    def __mul__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return self.numberInDecimal * otherInDecimal
    
    def __rmul__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return otherInDecimal * self.numberInDecimal
    
    def __mod__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return self.numberInDecimal % otherInDecimal
    
    def __rmod__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return otherInDecimal % self.numberInDecimal
    
    def __truediv__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return self.numberInDecimal / otherInDecimal
    
    def __rtruediv__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return otherInDecimal / self.numberInDecimal
    
    def __eq__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return self.numberInDecimal == otherInDecimal
    
    def __req__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return otherInDecimal == self.numberInDecimal
    
    def __ne__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return self.numberInDecimal != otherInDecimal
    
    def __rne__(self, other):
        otherInDecimal = self.convertOtherToDecimal(other)
        return otherInDecimal != self.numberInDecimal




# The instructions are not very clear as to what is desired, so I will interpret it as follows:
# The Client provides two numbers in baseX string form, e.g. "0P_123", and "0J_987", 
# and an operation to do with them, such as addition or subtraction, and the Server will return the result
# as a baseX string in decimal i.e. baseA, e.g. "0A_1110".
# The Server will expect to receive a comma-separated string in the form "number1,number2,operation", 
# where number1 and number2 are in baseX string form, and operation is a string, either "add", "sub", "mul" or "mod".
# For example, "0A_1,02_10,add". The Server will then send back a string in baseA form.

import socket
import re

class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 12346))

        self.sock.listen(1)
        print("Starting server...")
        print("Waiting for connection...")
        self.conn, addr = self.sock.accept()
        print("Connected...")

    def processClientMessage(self, clientMessage):
        # Split the message into number1, number2, and operation
        number1, number2, operation = clientMessage.split(',')
        number1 = BaseXNumber(number1)
        number2 = BaseXNumber(number2)
        result = 0
        if operation == 'add':
            result = number1 + number2
        elif operation == 'sub':
            result = number1 - number2
        elif operation == 'mul':
            result = number1 * number2
        elif operation == 'mod':
            result = number1 % number2
        result = BaseXNumber(result)
        result = result.getNumberInOriginalBase()
        return result

    def startProcessing(self):
        print("Start Processing")
        serverMessage = ''
        while True:
            data = self.conn.recv(1024)
            if data:
                clientResponse = data.decode('utf-8')
                print("Client:", clientResponse)
                if clientResponse.lower() == 'exit':
                    print("Client exited")
                    break
                serverMessage = self.processClientMessage(clientResponse)
                print("Server:", serverMessage)
                self.conn.sendall(serverMessage.encode('utf-8'))
        print("Exiting")
        print("Closing Connection")
        self.conn.close()

if __name__ == '__main__':

    print("Run some tests to validate the BaseX System: ")
    converter = BaseConverter()
    numbers = [BaseXNumber(36), BaseXNumber(123), BaseXNumber(456)]
    bases = [2, 8, 16]

    for number in numbers:
        print(f"\nTesting number {number}:")
        currNumber = number

        # Convert the number to each base
        for base in bases:
            print(f"\nConverting {currNumber.getNumberInOriginalBase()} to base {base}:")
            numInBase = BaseXNumber(converter.convert(currNumber.getNumberInOriginalBase(), base))
            print(f"Number {currNumber.getNumberInOriginalBase()} in base {base} is {numInBase.getNumberInOriginalBase()}")
            currNumber = numInBase

        print(f"\nConverting {currNumber.getNumberInOriginalBase()} back to base 10:")
        numInDecimal = BaseXNumber(converter.toDecimal(currNumber.getNumberInOriginalBase()))
        print(f"Number {currNumber.getNumberInOriginalBase()} is {numInDecimal.getNumberInOriginalBase()} in decimal")

        # Check if the number is the same after converting back to base 10
        if numInDecimal == number:
            print(f"Success: {numInDecimal.getNumberInOriginalBase()} == {number.getNumberInOriginalBase()}")
        else:
            print(f"Failure: {numInDecimal.getNumberInOriginalBase()} != {number.getNumberInOriginalBase()}")

    print("\n\n")

    # Do the Server/Client based testing

    print("Run the Server/Client based tests: ")
    server = Server()
    server.startProcessing()

    print("Done")
