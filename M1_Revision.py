'''
Rotating Caesar Cypher encryption and decryption
Mid 1 Q
'''


class Decryption:

    def __init__(self, shift=1, text="", asciiBegin = 0x20, asciiEnd = 0x80):
        self.shift = shift
        self.text = text
        self.encrypted = ""
        self.decrypted = ""
        self.asciiBegin = asciiBegin
        self.asciiEnd = asciiEnd
        self.caesarCypher()

    def caesarCypher(self):
        currShift = self.shift
        for char in self.text:
            asciiVal = ord(char)
            newAsciiVal = asciiVal + currShift
            if newAsciiVal > self.asciiEnd:
                newAsciiVal = newAsciiVal - self.asciiEnd + self.asciiBegin - 1
            self.encrypted += chr(newAsciiVal)
            currShift += 1
        return self.encrypted

    def decryptCaesarCypher(self):
        currShift = self.shift
        for char in self.encrypted:
            asciiVal = ord(char)
            newAsciiVal = asciiVal - currShift
            if newAsciiVal < self.asciiBegin:
                newAsciiVal = newAsciiVal + self.asciiEnd - self.asciiBegin + 1
            self.decrypted += chr(newAsciiVal)
            currShift += 1
        return self.decrypted

    def __len__(self):
        return len(self.encrypted)
    
    def __str__(self):
        if self.encrypted == "":
            print("No encrypted string found")
            return
        return self.encrypted
    
    def __getitem__(self, index):
        if self.encrypted == "":
            print("No encrypted string found")
            return
        return self.encrypted[index]
    
    def __iter__(self):
        if self.encrypted == "":
            print("No encrypted string found")
            return
        for char in self.encrypted:
            yield char
    
    '''
    Since the class is called Decryption, it seems appropriate that 
    __call__ should call the decrypt function
    '''
    def __call__(self, textIn=""):
        textToDecrypt = textIn
        if textIn == "":
            textToDecrypt = self.encrypted
        return self.decryptCaesarCypher()
    
    def __int__(self):
        return self.shift
    

    def __eq__(self, other):
        return (self.encrypted == other.encrypted)
    

# Main

stringToEncrypt = "Hello World"

print("Encrypt", stringToEncrypt)
decrypter = Decryption(5, stringToEncrypt)
print("Encrypted:", decrypter)

print("Decrypt", decrypter)
decryptedString = decrypter()
print("Decrypted:", decryptedString)


stringToEncrypt2 = "HELLO WORLD"

print("Encrypt", stringToEncrypt2)
decrypter2 = Decryption(5, stringToEncrypt2)
print("Encrypted:", decrypter2)

print("Decrypt", decrypter2)
decryptedString2 = decrypter2()
print("Decrypted:", decryptedString2)

print(f"{decrypter == decrypter2 = }")

