from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad
from base64 import b64encode
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
    MY_KEY_ID = 44
    (IV, ct) = real_oracle(MY_KEY_ID, b'Hello World!')
    print("IV = %s" % b64encode(IV))
    print("ct = %s" % b64encode(ct))
