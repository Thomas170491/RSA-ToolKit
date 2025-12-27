import sys
import os

# 1. Path Setup
# Ensure we can find our custom modules
sys.path.append(os.path.join(os.getcwd()))

# 2. Imports
from utils.rsa_math import generate_rsa_keys
from utils.padding import oaep_pad, oaep_unpad

def run_demonstration():
    print("-" * 50)
    print("RSA-OAEP CRYPTOSYSTEM DEMONSTRATION")
    print("-" * 50)

    # 3. Key Generation
    # We generate a 1024-bit modulus (n). 
    # k_size is 128 bytes (1024 / 8).
    bits = 1024
    k_size = bits // 8
    
    print(f"[*] Generating {bits}-bit RSA Keypair...")
    (e,n) , (d,n) = generate_rsa_keys(bits)
    print("[+] Keys generated successfully.")
    print(f"[*] Public Exponent (e): {e}")
    print(f"[*] Modulus (n) starts with: {str(n)[:20]}...")

    print("-" * 50)

    # 4. The Message
    message = "Secret Message for Thomas: The eagle has landed."
    print(f"Original Text:  {message}")
    message_bytes = message.encode('utf-8')

    # 5. Encryption Process
    # Text -> OAEP Pad -> Integer -> Modular Exponentiation
    print("[*] Applying OAEP Padding and Encrypting...")
    padded_block = oaep_pad(message_bytes, k_size)
    m_int = int.from_bytes(padded_block, byteorder='big')
    cipher_int = pow(m_int, e, n)
    
    print(f"Ciphertext (int): {str(cipher_int)[:60]}...")

    print("-" * 50)

    # 6. Decryption Process
    # Ciphertext -> Private Key Math -> Unpad -> Text
    print("[*] Decrypting and Removing OAEP Padding...")
    decrypted_int = pow(cipher_int, d, n)
    
    # We must ensure the byte string is exactly k_size (128 bytes) 
    # so the unpadding logic doesn't get misaligned.
    decrypted_padded_bytes = decrypted_int.to_bytes(k_size, byteorder='big')
    
    try:
        final_message_bytes = oaep_unpad(decrypted_padded_bytes, k_size)
        print(f"Decrypted Text: {final_message_bytes.decode('utf-8')}")
        print("[SUCCESS] Integrity check passed!")
    except ValueError as e:
        print(f"[FAILURE] Decryption failed: {e}")

    print("-" * 50)

if __name__ == "__main__":
    run_demonstration()