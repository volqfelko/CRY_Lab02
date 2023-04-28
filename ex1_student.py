from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad
from base64 import b64encode, b64decode
import secrets
import re
import socket

"""
This function queries the server with the specific key_id to encrypt
the plaintext. It returns the IV and the ciphertext as bytes.
Example:
>>> (IV, ct) = real_oracle(44, b'Hello World!')
>>> print("IV = %s" % b64encode(IV))
IV = b'roVEA/Wt8N7Ojp1GXEdb8w=='
>>> print("ct = %s" % b64encode(ct))
ct = b'HNly5YICj5mPh1LW3SLgNw=='

You can also contact the server manually with netcat:
$ nc iict-mv330-sfa.einet.ad.eivd.ch 8000 
Welcome to USB's encryption server

Please enter the encryption key ID: 44
Please enter the message in hex to encrypt: AAAA            

Encryption successful:
Message w/ padding: aaaa0e0e0e0e0e0e0e0e0e0e0e0e0e0e
IV                : ae854403f5adf0dece8e9d465c475bf0
Ciphertext        : edfab2e3f33b97de070a6c71f3dd0e34

Bye!
"""
def real_oracle(key_id: int, plaintext: bytes, host='iict-mv330-sfa.einet.ad.eivd.ch', port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # Wait for ID prompt
        while b'ID: ' not in s.recv(1024):
            pass
        s.sendall(str(key_id).encode('ascii') + b'\n')
        s.sendall(plaintext.hex().encode('ascii') + b'\n')
        # Read until we get b'Bye!'
        output = b''
        while b'Bye!' not in output:
            output += s.recv(1024)

        # Read the plaintext, iv and ciphertext
        output = output.decode('ascii')
        pt = re.findall(r'Message.*?: ([0-9a-fA-F]+)\n', output)
        iv = re.findall(r'IV.*?: ([0-9a-fA-F]+)\n', output)
        ct = re.findall(r'Ciphertext.*?: ([0-9a-fA-F]+)\n', output)

        # Ensure that we got exactly 3 regex matches
        if len(pt) + len(iv) + len(ct) != 3:
            raise Exception("Failed to get ciphertext")

        return bytes.fromhex(iv[0]), bytes.fromhex(ct[0])

if __name__ == "__main__":
    MY_KEY_ID = 65

    """
    print("IV = %s" % b64encode(IV))
    print("ct = %s" % b64encode(ct))
    """

    # Message chiffré intercepté
    ciphertext = b64decode(b'vA5rlBz+hcow8FWV6HvE8day2J8K9BjTRmfxfw4JxICcZuvrvOsduptvaeEPwqnSk3tytC3FwCUN5JfzxWYpdw==')
    # IV correspondant
    iv = b64decode(b'sRjQLv1OeyunLbF08XXDuQ==')

    # Known prefix and suffix of the plaintext
    prefix = b'Le salaire journalier du dirigeant USB est de '
    prefix2 = b'alier du dirigeant USB est de '
    suffix = b' CHF'

    #128 premiers bits du plain intercepté = b'Le salaire journ'
    plain_first_128_bits = prefix[:16]
    #IV_ref XOR plainText = b'/X3wXZwiGkLVSJEengCx1w=='
    alpha = strxor(iv, plain_first_128_bits)
    # 128 premiers bits du cipher intercepté = b'vA5rlBz+hcow8FWV6HvE8Q=='
    cipher_first_128_bits = ciphertext[:16]

    #Récuperation d'IV courant pour connaitre le prochain qui = IV + 1
    IV_courant, ciphertext_new = real_oracle(MY_KEY_ID, b'Hello World!')

    test = int.from_bytes(IV_courant, 'big') + 1
    IV_courant2 = test.to_bytes(16, 'big')

    # construction d'un plain qui XOR l'IV_courant + 1 = le XOR du message intercepté
    forged_plain = strxor(IV_courant2, alpha)
    print(forged_plain)
    print(b64encode(strxor(forged_plain, IV_courant2)))

    # Brute-force the salary value
    for salary in range(3001):
        m_first_128_int = int.from_bytes(forged_plain, 'big') - salary
        m_first_128_bits_new = m_first_128_int.to_bytes(16, 'big')
        print(f"salaire : {salary}")
        print(f"first bits : {b64encode(m_first_128_bits_new)}")

        plaintext = m_first_128_bits_new + prefix2 + str(salary).encode() + suffix
        plaintext = pad(plaintext, AES.block_size)
        IV, ciphertext_new = real_oracle(MY_KEY_ID, plaintext)
        
        print(plaintext)
        print(f"XOR forgé: {b64encode(ciphertext_new[:16])}")
        if ciphertext_new == ciphertext:
            print(f"The salary is: {salary}")
            break

    #Clé de 32 bytes donc 256 bits
    #AES 128 bits donc msg découpé en blocs de 128 bits (16 bytes)