'''
Rotating Caesar Cypher encryption and decryption
Mid 1 Q
'''

def caesarCypher(inputString, shift):
    outputString = ""
    for char in inputString:
        asciiVal = ord(char)
        newAsciiVal = asciiVal + shift
        if newAsciiVal > 0x80:
            newAsciiVal = newAsciiVal - 0x80 + 0x20 - 1
        outputString += chr(newAsciiVal)
        shift += 1
    return outputString


def decryptCaesarCypher(inputString, shift):
    outputString = ""
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
shift = 5
print("Encrypt", stringToEncrypt)
encryptedString = caesarCypher(stringToEncrypt, shift)
print(encryptedString)

print("Decrypt ", encryptedString)
decryptedString = decryptCaesarCypher(encryptedString, shift)
print(decryptedString)


