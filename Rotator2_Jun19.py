'''
Nathan Devlin
Rotator 2
June 19 2024
'''

class Rotor:
    def __init__(self, initialPosition=' ', incrementAmount=1, asciiBegin=0x20, asciiEnd=0x80):
        self.asciiBegin = asciiBegin
        self.asciiEnd = asciiEnd
        self.initialPosition = ord(initialPosition)
        self.position = ord(initialPosition)
        self.rotationCounter = 0
        self.incrementAmount = incrementAmount

    def reset(self):
        self.position = self.initialPosition
        self.rotationCounter = 0

    def increment(self):
        self.position += self.incrementAmount
        aboveEndAmount = self.position // self.asciiEnd
        self.position = (self.position % self.asciiEnd) + (aboveEndAmount * self.asciiBegin) - aboveEndAmount

    def decrement(self):
        self.position -= self.incrementAmount
        if self.position < self.asciiBegin:
            self.position = self.asciiEnd
    
    # Now returns a tuple with the character and a boolean telling if it went through a full rotation
    def rotate(self, char):
        didReset = False
        self.increment()
        asciiVal = ord(char)
        offset = self.position - self.asciiBegin
        newAsciiVal = asciiVal + offset

        aboveEndAmount = newAsciiVal // self.asciiEnd
        if aboveEndAmount > 0:
            didReset = True
        self.rotationCounter += aboveEndAmount
        newAsciiVal = (newAsciiVal % self.asciiEnd) + (aboveEndAmount * self.asciiBegin) - aboveEndAmount
        
        return (chr(newAsciiVal), didReset)
    
    def reverseRotate(self, char):
        didReset = False
        self.increment()
        asciiVal = ord(char)
        offset = self.position - self.asciiBegin

        newAsciiVal = asciiVal - offset
        if newAsciiVal < self.asciiBegin:
            newAsciiVal = self.asciiEnd - (self.asciiBegin - newAsciiVal) + 1
            self.rotationCounter += 1
            didReset = True

        return (chr(newAsciiVal), didReset)
    
    def counter(self):
        return self.rotationCounter

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


class Rotor2:
    def __init__(self, initialPosition=' ', incrementAmount=1, asciiBegin=0x20, asciiEnd=0x80):
        self.asciiBegin = asciiBegin
        self.asciiEnd = asciiEnd
        self.initialPosition = ord(initialPosition)
        self.position = ord(initialPosition)
        self.rotationCounter = 0
        self.incrementAmount = incrementAmount

    def reset(self):
        self.position = self.initialPosition
        self.rotationCounter = 0

    def increment(self):
        self.position += self.incrementAmount
        aboveEndAmount = self.position // self.asciiEnd
        self.position = (self.position % self.asciiEnd) + (aboveEndAmount * self.asciiBegin) - aboveEndAmount

    def decrement(self):
        self.position -= self.incrementAmount
        if self.position < self.asciiBegin:
            self.position = self.asciiEnd
        
    def rotate(self, char, increment=False):
        if increment:
            self.increment()
        asciiVal = ord(char)
        offset = self.position - self.asciiBegin
        newAsciiVal = asciiVal + offset

        aboveEndAmount = newAsciiVal // self.asciiEnd
        self.rotationCounter += aboveEndAmount
        newAsciiVal = (newAsciiVal % self.asciiEnd) + (aboveEndAmount * self.asciiBegin) - aboveEndAmount
        
        return chr(newAsciiVal)
    
    def reverseRotate(self, char, increment=False):
        if increment:
            self.increment()
        asciiVal = ord(char)
        offset = self.position - self.asciiBegin

        newAsciiVal = asciiVal - offset
        if newAsciiVal < self.asciiBegin:
            newAsciiVal = self.asciiEnd - (self.asciiBegin - newAsciiVal) + 1
            self.rotationCounter += 1
            didReset = True

        return chr(newAsciiVal)

    
    def counter(self):
        return self.rotationCounter

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
    def __init__(self, text=" ", initialPosition1=" ", intitialPosition2=" ", incrementAmount=1):
        self.text = text
        self.encrypted = ""
        self.decrypted = ""
        self.rotor1 = Rotor(initialPosition1, incrementAmount)
        self.rotor2 = Rotor2(intitialPosition2, incrementAmount)

    def caesarCypher(self):
        self.encrypted = ""
        for char in self.text:
            encryptedChar, didReset = self.rotor1.rotate(char)
            encryptedChar = self.rotor2.rotate(encryptedChar, didReset)
            self.encrypted += encryptedChar
        return self.encrypted

    def decryptCaesarCypher(self):
        self.decrypted = ""
        self.rotor1.reset()
        self.rotor2.reset()
        for char in self.encrypted:
            decryptedChar, didReset = self.rotor1.reverseRotate(char)
            decryptedChar = self.rotor2.reverseRotate(decryptedChar, didReset)
            self.decrypted += decryptedChar
        return self.decrypted


# Main

stringToEncrypt = "HELLO WORLDxyz+_)(*&^%$#@!{}~!"
print("Encrypt", stringToEncrypt)

decryption = Decryption(stringToEncrypt, "$")
decryption.caesarCypher()

print("Encrypted:", decryption.encrypted)

print("Decrypted:", decryption.decryptCaesarCypher())

