from Crypto.Cipher import AES
from Crypto.Util import Counter, strxor
from Crypto import Random
from base64 import b64encode


def cbcmac(message: bytes, key: bytes) -> bytes: 
    if len(key) !=  16:
        raise Exception("Error. Need key of 128 bits")
    if len(message) % 16 != 0:
        raise Exception("Error. Message needs to be a multiple of 128 bits")
    cipher = AES.new(key,AES.MODE_ECB)
    temp = b"\x00"*16
    blocks = [message[i:i+16] for i in range(0,len(message),16)]
    for b in blocks:
        temp = strxor.strxor(temp,b)
        temp = cipher.encrypt(temp)
    return temp

def ccm(message: bytes, key: bytes) -> tuple:
    """Encrypts with AES128-CCM without authenticated data. """

    if len(key) != 16:
        raise Exception("Only AES-128 is supported")

    cipher = AES.new(key, mode = AES.MODE_CTR)
    tag = cbcmac(message, key)
    ciphertext = cipher.encrypt(message)
    #Encrypt tag for security
    cipher = AES.new(key, mode = AES.MODE_CTR, nonce = cipher.nonce) #Reinitialize counter
    tag = cipher.encrypt(tag)
    return (cipher.nonce, ciphertext, tag)


if __name__ == "__main__":
    ra = Random.new()
    key  = ra.read(16)
    m1 = b"Ceci est un test"
    m2 = b"Ceci est un autre test plus long"
    (IV1, c1, tag1) = ccm(m1, key)
    (IV2, c2, tag2) = ccm(m2, key)
    print("m1 = %s" % m1)
    print("m2 = %s" % m2)
    print("c1 = %s" % b64encode(c1))
    print("IV1 = %s" % b64encode(IV1))
    print("tag1 = %s" % b64encode(tag1))
    print("c2 = %s" % b64encode(c2))
    print("IV2 = %s" % b64encode(IV2))
    print("tag2 = %s" % b64encode(tag2))

