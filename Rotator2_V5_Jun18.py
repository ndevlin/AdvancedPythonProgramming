'''
Nathan Devlin
Rotator 2 V5
June 18 2024
'''


class TwoLayerCaesarCipher:
    def __init__(self, initialPosLayer1=1, initialPosLayer2=1):
        self.initialPosLayer1 = initialPosLayer1
        self.initialPosLayer2 = initialPosLayer2
        self.currentPosLayer1 = initialPosLayer1
        self.currentPosLayer2 = initialPosLayer2

    def reset(self):
        self.currentPosLayer1 = self.initialPosLayer1
        self.currentPosLayer2 = self.initialPosLayer2
    

    # Verified
    def encryptCharacter(self, char):
        if char == "\n":
            return "\n"
        ordChar = ord(char) - 31
        encryptedChar = ordChar + self.currentPosLayer1
        if encryptedChar > 95:
            encryptedChar = encryptedChar % 96
            encryptedChar = encryptedChar + 1
        encryptedChar = encryptedChar + self.currentPosLayer2
        if encryptedChar > 95:
            encryptedChar = encryptedChar % 96
            encryptedChar = encryptedChar + 1
        self.currentPosLayer1 += 1
        if self.currentPosLayer1 > 95:
            self.currentPosLayer1 = 1
            self.currentPosLayer2 += 1
            if self.currentPosLayer2 > 95:
                self.currentPosLayer2 = 1
        newChar = chr(encryptedChar + 31)
        return newChar
    
    def encrypt(self, text):
        result = ""
        for char in text:
            result += self.encryptCharacter(char)
        return result

    # Verified
    def decryptCharacter(self, char):
        #print("charIn: ", char)
        if char == "\n":
            return "\n"
        ordChar = ord(char) - 31
        self.currentPosLayer1 -= 1
        if self.currentPosLayer1 < 1:
            self.currentPosLayer1 = 95
            self.currentPosLayer2 -= 1
            if self.currentPosLayer2 < 1:
                self.currentPosLayer2 = 95
        decryptedChar = ordChar - self.currentPosLayer2
        if decryptedChar < 1:
            decryptedChar = decryptedChar + 95
        decryptedChar = decryptedChar - self.currentPosLayer1
        if decryptedChar < 1:
            decryptedChar = decryptedChar + 95
        newChar = chr(decryptedChar + 31)
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
cypher = TwoLayerCaesarCipher(1,1)
text = "Alan Turing, an English mathematician, logician, and cryptanalyst, was a computer pioneer. Often remembered for his contributions to the fields of artificial intelligence and modern computer science before either even existed, Turing is probably best known for what is now dubbed the Turing Test. It is a process of testing a machines ability to think. The basic premise of the Turing Test is that a human judge would be placed in isolation and have two conversations - one with a computer and one with another person - except the judge wouldn’t be told which was which. If the computer could fool the judge and carry on a conversation that is indistinguishable from that of the human, the computer is said to have passed the Turing Test. Less is known, however, about Turing’s intelligence work during WWII when he used his mathematical and cryptologic skills to help break one of the most difficult of German ciphers, ENIGMA. ENIGMA was a cipher machine—each keystroke replaced a character in the message with another character determined by the machine’s rotor settings and wiring arrangements that were previously established between the sender and the receiver."
print(f"Original: {text}")
encrypted = cypher.encrypt(text)
print(f"Encrypted: {encrypted}")


cypher2 = TwoLayerCaesarCipher(27,13)
decrypted = cypher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

print("Brute Force Decryption: ")

characterPercentages = {" ": 16, "e": 10, "t": 7, "i": 6, "a": 6}

textFromFile = ''
filePath = 'E2Rotor.txt'
with open(filePath, 'r') as file:
    textFromFile = file.read()

numChars = len(textFromFile)
print(f"{numChars = }")

print("\n")

if True:
    for i in range(1, 96):
        for j in range(1, 96):
            cypher = TwoLayerCaesarCipher(i, j)
            decrypted = cypher.decrypt(textFromFile)

            multiplier = 0.4

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

            if pastThreshold:
                print(decrypted)
                print(f"End Pos Layer 1: {j}", f"End Pos Layer 2: {i}")
                print("\n")




