from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES
import sys
from base64 import b64decode

KEY_SIZE = 2 #In bytes


if __name__ == "__main__":
    ra = Random.new()
    key1 = ra.read(KEY_SIZE) + (32 - KEY_SIZE) * b"\x00"
    AES1 = AES.new(key1, AES.MODE_ECB)
    key2 = ra.read(KEY_SIZE) + (32 - KEY_SIZE) * b"\x00"
    AES2 = AES.new(key2, AES.MODE_ECB)
    plaintext = ra.read(AES.block_size)
    ciphertext = AES2.encrypt(AES1.encrypt(plaintext))
    print("plaintext = %s" % b64encode(plaintext))
    print("ciphertext = %s" % b64encode(ciphertext))
    print("key1 = %s" % b64encode(key1), file=sys.stderr)
    print("key2 = %s" % b64encode(key2), file=sys.stderr)

    plaintext = b64decode(b'/JlEx61dBJQvIOfCZTGyHw==')
    ciphertext = b64decode(b'iy5TSaqXDq62UizAtZfb7w==')

    key1_initial = b"\x00\x00" + (30 * b"\x00")
    key2_initial = b"\x00\x00" + (30 * b"\x00")

    results = {}

    for i in range(2 ** 16):
        key1 = i.to_bytes(2, byteorder='big') + (30 * b"\x00")
        AES1 = AES.new(key1, AES.MODE_ECB)
        for j in range(2 ** 16):
            key2 = j.to_bytes(2, byteorder='big') + (30 * b"\x00")
            if key2 in results:
                decrypted = AES1.decrypt(results[key2])
            else:
                AES2 = AES.new(key2, AES.MODE_ECB)
                decrypted = AES1.decrypt(AES2.decrypt(ciphertext))
                results[key2] = AES2.encrypt(decrypted)
            if decrypted == plaintext:
                print("key1 = %s" % b64encode(key1))
                print("key2 = %s" % b64encode(key2))
                break
