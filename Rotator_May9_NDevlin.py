'''
Nathan Devlin
Rotator Exercise
May 9 2024
'''

class Rotor:
    def __init__(self, initialPosition=' ', incrementAmount=1, asciiBegin=0x20, asciiEnd=0x80):
        self.asciiBegin = asciiBegin
        self.asciiEnd = asciiEnd
        self.initialPosition = ord(initialPosition)
        self.position = ord(initialPosition)
        self.counter = 0
        self.incrementAmount = incrementAmount

    def reset(self):
        self.position = self.initialPosition
        self.counter = 0

    def increment(self):
        self.position += self.incrementAmount
        if self.position > self.asciiEnd:
            self.position = self.asciiBegin

    def decrement(self):
        self.position -= self.incrementAmount
        if self.position < self.asciiBegin:
            self.position = self.asciiEnd

    def rotate(self, char):
        self.increment()
        asciiVal = ord(char)
        offset = self.position - self.asciiBegin
        newAsciiVal = asciiVal + offset
        if newAsciiVal > self.asciiEnd:
            newAsciiVal = newAsciiVal - self.asciiEnd + self.asciiBegin - 1
            self.counter += 1
        return chr(newAsciiVal)
    
    def reverseRotate(self, char):
        self.increment()
        asciiVal = ord(char)
        offset = self.position - self.asciiBegin
        newAsciiVal = asciiVal - offset
        if newAsciiVal < self.asciiBegin:
            newAsciiVal = self.asciiEnd - (self.asciiBegin - newAsciiVal) + 1
            self.counter += 1
        return chr(newAsciiVal)
    
    def counter(self):
        return self.counter

    def __str__(self):
        return chr(self.position)
    
    def __eq__(self, other):
        if isinstance(other, Rotor):
            return self.position == other.position and \
            self.asciiBegin == other.asciiBegin and \
            self.asciiEnd == other.asciiEnd and \
            self.initialPosition == other.initialPosition and \
            self.position == other.position and \
            self.incrementAmount == other.incrementAmount
        return False


class Decryption:
    def __init__(self, text=" ", initialPosition=" ", incrementAmount=1):
        self.text = text
        self.encrypted = ""
        self.decrypted = ""
        self.rotor = Rotor(initialPosition, incrementAmount)
        self.caesarCypher()

    def caesarCypher(self):
        self.encrypted = ""
        for char in self.text:
            self.encrypted += self.rotor.rotate(char)
        return self.encrypted

    def decryptCaesarCypher(self):
        self.decrypted = ""
        self.rotor.reset()
        for char in self.encrypted:
            self.decrypted += self.rotor.reverseRotate(char)
        return self.decrypted


# Main

stringToEncrypt = "HELLO WORLD!"
print("Encrypt", stringToEncrypt)

decryption = Decryption(stringToEncrypt, "$")
print("Encrypted:", decryption.encrypted)

print("Decrypted:", decryption.decryptCaesarCypher())

