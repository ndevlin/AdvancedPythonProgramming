'''
Nathan Devlin
Rotator 2 V4
June 21 2024
'''

class Rotor:
    def __init__(self, initialPos=" "):
        self.currentPos = self.convertCharToNum(initialPos)
    
    # For simplicity, assign valid characters to numbers 1-95
    def convertCharToNum(self, char):
        if type(char) != str:
            return char
        return ord(char) - 31
    
    def convertNumToChar(self, num):
        if type(num) != int:
            return num
        return chr(num + 31)

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

class TwoLayerCaesarCipher:
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
    
# Main code to demonstrate encryption and decryption
cypher = TwoLayerCaesarCipher()
text = "Hello, World!~ *#}!"
print(f"Original: {text}")
encrypted = cypher.encrypt(text)
print(f"Encrypted: {encrypted}")
decrypted = cypher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

textFromFile = ''
filePath = 'TestEncryptedText.txt'
with open(filePath, 'r') as file:
    textFromFile = file.read()


newTextFromFile = ""
for char in textFromFile:
    if char != "\n":
        newTextFromFile += char
textFromFile = newTextFromFile

numChars = len(textFromFile)
print(f"{numChars = }")

print(f"{len(textFromFile) = }")

print("\n")

print("Brute Force Decryption: ")

characterPercentages = {" ": 16, "e": 10, "t": 7, "i": 6, "a": 6}

listOfDecryptedTexts = []


for i in range(1, 96):
    for j in range(1, 96):
        cypher = TwoLayerCaesarCipher(i, j)
        decrypted = cypher.decrypt(textFromFile)

        multiplier = 0.9

        numSpaces = 0
        numEs = 0
        numTs = 0
        numIs = 0
        numAs = 0
        for char in decrypted:
            if char == " ":
                numSpaces += 1
            if char == "e":
                numEs += 1
            if char == "t":
                numTs += 1
            if char == "i":
                numIs += 1
            if char == "a":
                numAs += 1
        pastThreshold = False

        if numSpaces > 188 * multiplier:
            if numEs > 118 * multiplier:
                if numTs > 82 * multiplier:
                    if numIs > 74 * multiplier:
                        if numAs > 70 * multiplier:
                            pastThreshold = True

        testText = "Alan Turing, an English mathematician, logician, and cryptanalyst, was a computer pioneer."

        if pastThreshold:
            listOfDecryptedTexts.append(decrypted)
            print(decrypted)
            print(f"Initial Pos Layer 1: {j}", f"Initial Pos Layer 2: {i}")
            print("\n")




