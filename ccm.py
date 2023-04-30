from Crypto.Cipher import AES
from Crypto.Util import Counter, strxor
from Crypto import Random
from base64 import b64encode


def cbcmac(message: bytes, key: bytes) -> bytes:
    if len(key) != 16:
        raise Exception("Error. Need key of 128 bits")
    if len(message) % 16 != 0:
        raise Exception("Error. Message needs to be a multiple of 128 bits")
    cipher = AES.new(key, AES.MODE_ECB)
    temp = b"\x00"*16
    blocks = [message[i:i+16] for i in range(0, len(message), 16)]
    for b in blocks:
        temp = strxor.strxor(temp, b)
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
    key = ra.read(16)

    m1 = b"Ceci est un test"
    m2 = b"Ceci est un test mais plus long "
    print(len(m1))
    (IV1, c1, tag1) = ccm(m1, key)
    (IV2, c2, tag2) = ccm(m2, key)
    print(b64encode(tag1))

    #Récuperation du tag1 original déchiffré
    keystream = strxor.strxor(m1, c1)
    original_tag = strxor.strxor(tag1, keystream)

    #Déchiffrement du tag1 pour comparer avec celui calculé
    cipher = AES.new(key, mode=AES.MODE_CTR, nonce=IV1)
    original_tag_decrypted = cipher.decrypt(tag1)

    if original_tag == original_tag_decrypted:
        print("TAG calculé == TAG original !! ")
        print("TAG calculé = " + str(b64encode(original_tag)) + " ¦¦ TAG original = " + str(b64encode(original_tag_decrypted)))

    message_forged = m1 + strxor.strxor(m1, original_tag)
    tag_forged = cbcmac(message_forged, key)

    if original_tag == tag_forged:
        print("\nTAG forgé == TAG original !! ")
        print("TAG forgé = " + str(b64encode(tag_forged)) + " ¦¦ TAG original = " + str(b64encode(original_tag)))
        print("Message forgé = " + str(message_forged) + " ¦¦ Message original = " + str(m1))

