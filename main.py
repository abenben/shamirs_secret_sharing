from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.SecretSharing import Shamir
from binascii import hexlify
from base64 import b64encode

# Load file data
with open('memo.txt', 'rb') as file:
    file_data = file.read()

# AES Encryption (if you want to encrypt the file data)
key = get_random_bytes(16)  # Generate a 16-byte random key
cipher = AES.new(key, AES.MODE_CFB)
ciphered_data = cipher.encrypt(file_data)

# Convert to a format suitable for Shamir's Secret Sharing
# Example: Use the first 16 bytes of ciphered data
# Ensure this data is critical for decryption or represents your actual secret
secret_data = ciphered_data[:16]

# Split the secret
shares = Shamir.split(2, 3, secret_data)

# Save the shares
for idx, share in shares:
    with open(f'./works/share_{idx}.txt', 'wb') as share_file:
        share_file.write(share)
        print("Index #%d: %s" % (idx, hexlify(share)))
