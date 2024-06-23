'''
Nathan Devlin
Rotator 2 V2
June 20 2024
'''


class TwoLayerCaesarCipher:
    def __init__(self, initial_pos_layer1=0x20, initial_pos_layer2=0x20):
        self.initial_pos_layer1 = initial_pos_layer1
        self.initial_pos_layer2 = initial_pos_layer2
        self.current_pos_layer1 = initial_pos_layer1
        self.current_pos_layer2 = initial_pos_layer2

    def encrypt_character(self, char):
        # Encrypt with first layer
        encrypted_char = chr(((ord(char) + self.current_pos_layer1) % 0x7F) % (0x7F + 0x20))
        self.current_pos_layer1 += 1
        if self.current_pos_layer1 > 0x7F:
            self.current_pos_layer1 = 0x20
            self.current_pos_layer2 += 1
            if self.current_pos_layer2 > 0x7F:
                self.current_pos_layer2 = 0x20

        # Encrypt with second layer
        encrypted_char = chr(((ord(encrypted_char) + self.current_pos_layer2) % 0x7F) % (0x7F + 0x20))
        return encrypted_char

    def encrypt(self, text):
        return ''.join([self.encrypt_character(char) for char in text])
    
    def decrypt_character(self, char):
        # Reverse the process of the first layer
        decrypted_char = chr(((ord(char) - self.current_pos_layer2 - 0x20) % 0x5F) + 0x20)
        
        # Adjust the second layer position
        self.current_pos_layer2 -= 1
        if self.current_pos_layer2 < 0x20:
            self.current_pos_layer2 = 0x7E  # Adjusted to 0x7E for correct wrap-around

        # Then reverse the process of the second layer
        decrypted_char = chr(((ord(decrypted_char) - self.current_pos_layer1 - 0x20) % 0x5F) + 0x20)

        # Adjust the first layer position
        self.current_pos_layer1 -= 1
        if self.current_pos_layer1 < 0x20:
            self.current_pos_layer1 = 0x7E  # Adjusted to 0x7E for correct wrap-around

        return decrypted_char

    def decrypt(self, text):
        # Ensure we decrypt in the forward order, not reversed
        decrypted_text = ''.join([self.decrypt_character(char) for char in text])
        # Reset positions after decryption to match encryption start state
        self.current_pos_layer1 = self.initial_pos_layer1
        self.current_pos_layer2 = self.initial_pos_layer2
        return decrypted_text

# Main code to demonstrate encryption and decryption
if __name__ == "__main__":
    cipher = TwoLayerCaesarCipher()
    original_text = "HEllo Dig Dagitty WOrld!&%*()^#&(~+ )"
    print("Original:", original_text)
    encrypted_text = cipher.encrypt(original_text)
    print("Encrypted:", encrypted_text)
    # Reset cipher state before decryption
    cipher = TwoLayerCaesarCipher()  # Resetting to ensure decryption starts with initial positions
    decrypted_text = cipher.decrypt(encrypted_text)
    print("Decrypted:", decrypted_text)