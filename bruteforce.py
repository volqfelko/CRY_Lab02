from Crypto.Cipher import AES
from base64 import b64decode, b64encode

KEY_SIZE = 2 #In bytes


if __name__ == "__main__":
    plaintext = b64decode(b'/JlEx61dBJQvIOfCZTGyHw==')
    ciphertext = b64decode(b'iy5TSaqXDq62UizAtZfb7w==')

    #Meet-in-the-Middle attack
    possible_outputs = {}
    for i in range(2 ** 16):
        key1 = i.to_bytes(2, byteorder='big') + (30 * b"\x00")
        aes = AES.new(key1, AES.MODE_ECB)
        possible_outputs[aes.encrypt(plaintext)] = key1

    for intermediate in possible_outputs.keys():
        aes = AES.new(possible_outputs[intermediate], AES.MODE_ECB)
        decrypted = aes.decrypt(ciphertext)
        if decrypted in possible_outputs:
            key1 = possible_outputs[intermediate]
            key2 = possible_outputs[decrypted]
            print(f"KEYS FOUND !!! Key 1: {b64encode(key1)}, Key 2: {b64encode(key2)}")
            break