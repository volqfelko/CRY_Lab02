from base64 import b64encode
from Crypto import Random
from Crypto.Cipher import AES
import sys

KEY_SIZE = 2 #In bytes       


if __name__ == "__main__":
    ra = Random.new()
    key1 = ra.read(KEY_SIZE)+(32 - KEY_SIZE)*b"\x00"
    AES1 = AES.new(key1, AES.MODE_ECB)
    key2 = ra.read(KEY_SIZE)+(32 - KEY_SIZE)*b"\x00"
    AES2 = AES.new(key2, AES.MODE_ECB)
    plaintext = ra.read(AES.block_size)
    ciphertext = AES2.encrypt(AES1.encrypt(plaintext))
    print("plaintext = %s" % b64encode(plaintext))
    print("ciphertext = %s" % b64encode(ciphertext))
    print("key1 = %s" % b64encode(key1), file=sys.stderr)
    print("key2 = %s" % b64encode(key2), file=sys.stderr)

