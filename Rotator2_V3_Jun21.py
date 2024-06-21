'''
Nathan Devlin
Rotator 2 V3
June 21 2024
'''


class TwoLayerCaesarCipher:
    def __init__(self, initialPosLayer1=0x20, initialPosLayer2=0x20):
        self.initialPosLayer1 = initialPosLayer1
        self.initialPosLayer2 = initialPosLayer2
        self.currentPosLayer1 = initialPosLayer1
        self.currentPosLayer2 = initialPosLayer2

    def reset(self):
        self.currentPosLayer1 = self.initialPosLayer1
        self.currentPosLayer2 = self.initialPosLayer2
    
    def encryptCharacter(self, char):
        if char == "\n":
            return "\n"
        ordChar = ord(char)
        ecryptedChar = ordChar + self.currentPosLayer1
        while ecryptedChar > 0x7E:
            ecryptedChar = ecryptedChar - 0x5F
        ecryptedChar = ecryptedChar + self.currentPosLayer2
        while ecryptedChar > 0x7E:
            ecryptedChar = ecryptedChar - 0x5F
        self.currentPosLayer1 += 1
        while self.currentPosLayer1 > 0x7E:
            self.currentPosLayer1 = 0x20
            self.currentPosLayer2 += 1
            while self.currentPosLayer2 > 0x7E:
                self.currentPosLayer2 = 0x20
        newChar = chr(ecryptedChar)
        return newChar
    
    def encrypt(self, text):
        result = ""
        for char in text:
            result += self.encryptCharacter(char)
        return result

    def decryptCharacter(self, char):
        #print("charIn: ", char)
        if char == "\n":
            return "\n"
        #if char == "u":
            #print("We gotta u")
        self.currentPosLayer1 -= 1
        ordChar = ord(char)
        decryptedChar = ordChar - self.currentPosLayer2
        while decryptedChar < 0x20:
            decryptedChar = decryptedChar + 0x5F
        decryptedChar = decryptedChar - self.currentPosLayer1
        while decryptedChar < 0x20:
            decryptedChar = decryptedChar + 0x5F
        while self.currentPosLayer1 < 0x20:
            self.currentPosLayer1 = 0x7E
            self.currentPosLayer2 -= 1
        while self.currentPosLayer2 < 0x20:
            self.currentPosLayer2 = 0x7E
        newChar = chr(decryptedChar)
        #print("charOut: ", newChar)
        return newChar
    
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
text = "HEllo Dig Dagitty WOrld!&%*()^#&(~+ )"
print(f"Original: {text}")
encrypted = cypher.encrypt(text)
print(f"Encrypted: {encrypted}")
decrypted = cypher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

textFromFile = ''
filePath = 'E2Rotor.txt'
with open(filePath, 'r') as file:
    textFromFile = file.read()

print(textFromFile)

print("\n")

print("Brute Force Decryption: ")

listOfDecryptedTexts = []

for i in range(0x20, 0x7F):
    for j in range(0x20, 0x7F):
        cypher = TwoLayerCaesarCipher(j, i)
        decrypted = cypher.decrypt(textFromFile)

        numSpaces = 0
        for char in decrypted:
            if char == " ":
                numSpaces += 1
        if numSpaces > 94:
            listOfDecryptedTexts.append(decrypted)
            print(decrypted)
            print(f"Initial Pos Layer 1: {j}", f"Initial Pos Layer 2: {i}")


