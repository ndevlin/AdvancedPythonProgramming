'''
Rotator for Command, CaesarCypherClient and RotatorServer
May 24 2024
'''

class Rotor:
    def __init__(self, initialPosition='$', incrementAmount=1, asciiBegin=0x20, asciiEnd=0x80):
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
