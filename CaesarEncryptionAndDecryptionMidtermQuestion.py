'''
Rotating Caesar Cypher encryption and decryption
Mid Q 1
'''

def rotating_caesar_cipher(input_string, shift):
    output_string = ""
    for char in input_string:
        ascii_val = ord(char)
        new_ascii_val = ascii_val + shift
        if new_ascii_val > 0x80:
            new_ascii_val = new_ascii_val - 0x80 + 0x20 - 1
        output_string += chr(new_ascii_val)
        shift += 1
    return output_string


def decrypt_rotating_caesar_cipher(input_string, shift):
    output_string = ""
    for char in input_string:
        ascii_val = ord(char)
        if 0x20 <= ascii_val <= 0x80:
            new_ascii_val = ascii_val - shift
            if new_ascii_val < 0x20:
                new_ascii_val = new_ascii_val + 0x80 - 0x20 + 1
            output_string += chr(new_ascii_val)
            shift += 1
        else:
            output_string += char
    return output_string


# Main

stringToEncrypt = "HELLO"
shift = 5
print("Encrypt", stringToEncrypt)
encryptedString = rotating_caesar_cipher(stringToEncrypt, shift)
print(encryptedString)

print("Decrypt ", encryptedString)
decryptedString = decrypt_rotating_caesar_cipher(encryptedString, shift)
print(decryptedString)


