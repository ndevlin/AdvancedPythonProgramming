'''
Nathan Devlin
Rotator 2
June 18 2024
'''

from time import sleep

class Rotor:
    def __init__(self, initialPos=" "):
        self.currentPos = self.convertCharToNum(initialPos)
    
    # For simplicity, assign valid characters to numbers 1-95
    # Valid chars are considered to be the ASCII characters between " " and "~"
    def convertCharToNum(self, char):
        if type(char) != str:
            return char - 31
        return ord(char) - 31
    
    def convertNumToChar(self, num):
        if type(num) != int:
            return num + 31
        return chr(num + 31)

    def getPos(self):
        return self.convertNumToChar(self.currentPos)

    def reset(self, resetPos=" "):
        self.currentPos = self.convertCharToNum(resetPos)
    
    def encryptChar(self, char):
        if char == "\n":
            return "\n"
        ordChar = self.convertCharToNum(char)
        encryptedChar = ordChar + self.currentPos
        if encryptedChar > 95:
            encryptedChar = encryptedChar % 96
            encryptedChar = encryptedChar + 1
        newChar = self.convertNumToChar(encryptedChar)
        return newChar
    
    # Returns True if it has looped back to the beginning, False otherwise
    def increment(self):
        self.currentPos += 1
        if self.currentPos > 95:
            self.currentPos = 1
            return True
        return False
    
    def decryptChar(self, char):
        if char == "\n":
            return "\n"
        ordChar = self.convertCharToNum(char)
        decryptedChar = ordChar - self.currentPos
        if decryptedChar < 1:
            decryptedChar = decryptedChar + 95
        newChar = self.convertNumToChar(decryptedChar)
        return newChar
    
    # Returns True if it has looped back to the end, False otherwise
    def decrement(self):
        self.currentPos -= 1
        if self.currentPos < 1:
            self.currentPos = 95
            return True
        return False


class TwoLayerCaesarCypher:
    def __init__(self, initialPosLayer1=" ", initialPosLayer2=" "):
        self.initialPosLayer1 = initialPosLayer1
        self.rotor1 = Rotor(initialPosLayer1)
        self.initialPosLayer2 = initialPosLayer2
        self.rotor2 = Rotor(initialPosLayer2)

    def reset(self):
        self.rotor1.reset(self.initialPosLayer1)
        self.rotor2.reset(self.initialPosLayer2)
    
    def encryptCharacter(self, char):
        encryptedChar = self.rotor1.encryptChar(char)
        encryptedChar = self.rotor2.encryptChar(encryptedChar)
        if self.rotor1.increment():
            self.rotor2.increment()
        return encryptedChar
    
    def encrypt(self, text):
        result = ""
        for char in text:
            result += self.encryptCharacter(char)
        return result

    def decryptCharacter(self, char):
        if self.rotor1.decrement():
            self.rotor2.decrement()
        decryptedChar = self.rotor1.decryptChar(char)
        decryptedChar = self.rotor2.decryptChar(decryptedChar)
        return decryptedChar
    
    def decrypt(self, text):
        # First reverse the order of the text
        text = text[::-1]
        result = ""
        for char in text:
            result += self.decryptCharacter(char)
        # Un-reverse the text
        result = result[::-1]
        self.reset()
        return result
    
    def calculateInitialPositionsFromFinalPositions(self, text, finalPosLayer1, finalPosLayer2):
        testRotor1 = Rotor(finalPosLayer1)
        testRotor2 = Rotor(finalPosLayer2)
        for char in text:
            if testRotor1.decrement():
                testRotor2.decrement()
        return testRotor1.getPos(), testRotor2.getPos()
    

# Main code to demonstrate encryption and decryption
cypher = TwoLayerCaesarCypher()
text = "Hello, World!~ *#}!"
print(f"Original: {text}")
encrypted = cypher.encrypt(text)
print(f"Encrypted: {encrypted}")
rotor1FinalPos = cypher.rotor1.getPos()
print(f"{rotor1FinalPos = }")
rotor2FinalPos = cypher.rotor2.getPos()
print(f"{rotor2FinalPos = }")
initialPositions = cypher.calculateInitialPositionsFromFinalPositions(encrypted, rotor1FinalPos, rotor2FinalPos)
print(f"{initialPositions = }")
decrypted = cypher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")


# Test decrypt text from a file
# Enryption and Decryption appears to work with the text. Something seems off with the E2Rotor.txt file
print("\n")
print("Test Read from File: ")

unEncrypted = ''
with open("TestEncryptedTextOriginalUnEncrypted.txt", 'r') as file:
    unEncrypted = file.read()

textFromFile = ''
filePath = 'TestEncryptedText.txt'
with open(filePath, 'r') as file:
    textFromFile = file.read()

numChars = len(textFromFile)
print(f"{numChars = }")

print("\n")
print(f"Original: {unEncrypted}")

cypher2 = TwoLayerCaesarCypher(" ", " ")
encrypted2 = cypher2.encrypt(unEncrypted)
rotor1FinalPos = cypher2.rotor1.getPos()

print("\n")
print(f"Encrypted: {encrypted2}")
print("\n")

print(f"{rotor1FinalPos = }")
rotor2FinalPos = cypher2.rotor2.getPos()
print(f"{rotor2FinalPos = }")
initialPositions = cypher.calculateInitialPositionsFromFinalPositions(encrypted2, rotor1FinalPos, rotor2FinalPos)
print(f"{initialPositions = }")
print("\n")

# We are reading from TestEncryptedText.txt, which is the encrypted version of TestEncryptedTextOriginalUnEncrypted.txt
# This appears to work almost flawlessly
cypher2 = TwoLayerCaesarCypher(chr(ord(rotor1FinalPos) - 1), rotor2FinalPos)
decrypted2 = cypher2.decrypt(textFromFile)
print(f"Decrypted: {decrypted2}")



print("\n")
print("Use E2Rotor.txt: ")
print("Attempt to decrypt with default values: ")
print("\n")

e2Rotor = ''
filePath = 'E2Rotor.txt'
with open(filePath, 'r') as file:
    e2Rotor = file.read()

numChars = len(e2Rotor)
print(f"{numChars = }")
print("\n")
print(f"Original: {e2Rotor}")
print("\n")

# Use a dummy Cypher using the same number of characters as the encrypted text to calculate the ending postions of the rotors
dummyCypher = TwoLayerCaesarCypher(" ", " ")
dummyEncrypted = dummyCypher.encrypt(e2Rotor)
rotor1FinalPos = dummyCypher.rotor1.getPos()
print(f"{rotor1FinalPos = }")
rotor2FinalPos = dummyCypher.rotor2.getPos()
print(f"{rotor2FinalPos = }")
initialPositions = dummyCypher.calculateInitialPositionsFromFinalPositions(dummyEncrypted, rotor1FinalPos, rotor2FinalPos)
print(f"{initialPositions = }")
print("\n")

cypher3 = TwoLayerCaesarCypher(rotor1FinalPos, rotor2FinalPos)
decrypted3 = cypher3.decrypt(e2Rotor)
rotor1FinalPos = cypher3.rotor1.getPos()
print(f"Decrypted: {decrypted3}")

print("\n")
print(f"{rotor1FinalPos = }")
rotor2FinalPos = cypher3.rotor2.getPos()
print(f"{rotor2FinalPos = }")
initialPositions = cypher3.calculateInitialPositionsFromFinalPositions(dummyEncrypted, rotor1FinalPos, rotor2FinalPos)
print(f"{initialPositions = }")
# We successfully decrypt "Alan Turing at the start of the file. It seems something else has gone awry with the E2Rotor.txt file after that"

sleep(2)

print("\n")
print("\n")
print("Brute Force Decryption: ")

lastMatch = 0

if True:
    print("Start Brute Force Decryption")
    for i in range(ord(" "), ord("~") + 1):
        for j in range(ord(" "), ord("~") + 1):
            cypher4 = TwoLayerCaesarCypher(i, j)
            decrypted4 = cypher4.decrypt(e2Rotor)

            numSpaces = 0
            numEs = 0
            numAs = 0
            numRs = 0
            numIs = 0

            for char in decrypted4:
                if char == " ":
                    numSpaces += 1
                if char == "e":
                    numEs += 1
                if char == "a":
                    numAs += 1
                if char == "r":
                    numRs += 1
                if char == "i":
                    numIs += 1

            percentSpaces = numSpaces / numChars
            percentEs = numEs / numChars
            percentAs = numAs / numChars
            percentRs = numRs / numChars
            percentIs = numIs / numChars
            percentMatch = percentSpaces + percentEs + percentAs + percentRs + percentIs

            threshold = 0.1

            if percentMatch > threshold and percentMatch > lastMatch:
                print(f"{percentMatch = }")
                lastMatch = percentMatch
                print(decrypted4)
                print(f"Pos Layer 1: {j}", f"Pos Layer 2: {i}")
                rotor1FinalPos = cypher4.rotor1.getPos()
                print(f"{rotor1FinalPos = }")
                rotor2FinalPos = cypher4.rotor2.getPos()
                print(f"{rotor2FinalPos = }")
                initialPositions = cypher4.calculateInitialPositionsFromFinalPositions(decrypted4, rotor1FinalPos, rotor2FinalPos)
                print(f"{initialPositions = }")

                print("\n")

# The closest match is the last one to be printed. The final rotor positions and initial rotor positions are printed as well


