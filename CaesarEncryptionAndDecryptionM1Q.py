'''
Rotating Caesar Cypher encryption and decryption
Mid 1 Q
'''

class Decryption:

    def __init__(self, shift):
        self.shift = shift

    def caesarCypher(self, inputString):
        outputString = ""
        shift = self.shift
        for char in inputString:
            asciiVal = ord(char)
            newAsciiVal = asciiVal + shift
            if newAsciiVal > 0x80:
                newAsciiVal = newAsciiVal - 0x80 + 0x20 - 1
            outputString += chr(newAsciiVal)
            shift += 1
        return outputString

    def decryptCaesarCypher(self, inputString):
        outputString = ""
        shift = self.shift
        for char in inputString:
            asciiVal = ord(char)
            newAsciiVal = asciiVal - shift
            if newAsciiVal < 0x20:
                newAsciiVal = newAsciiVal + 0x80 - 0x20 + 1
            outputString += chr(newAsciiVal)
            shift += 1
        return outputString


# Main

stringToEncrypt = "HELLO"

decrypter = Decryption(shift=5)

print("Encrypt", stringToEncrypt)
encryptedString = decrypter.caesarCypher(stringToEncrypt)
print(encryptedString)

print("Decrypt ", encryptedString)
decryptedString = decrypter.decryptCaesarCypher(encryptedString)
print(decryptedString)


