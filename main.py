import sys
import os

# Ensure we can find our custom modules in the current directory
sys.path.append(os.path.join(os.getcwd()))

from utils.rsa_math import generate_rsa_keys
from utils.padding import oaep_pad, oaep_unpad
from utils.signatures import pss_encode, pss_verify

def run_demonstration():
    # --- 1. SETUP ---
    bits = 1024
    # k_size is the length of the modulus in bytes
    k_size = bits // 8
    
    print("=" * 60)
    print(f"RSA TOOLKIT DEMO: {bits}-BIT MODULUS")
    print("=" * 60)
    
    print(f"[*] Generating Keypair...")
    (d,n), (e,n)= generate_rsa_keys(bits)
    
    # We recalculate k_size based on the actual bit length of n
    # This prevents OverflowErrors if n is exactly 1024 bits
    byte_len = (n.bit_length() + 7) // 8
    
    print("[+] Public and Private keys generated.")
    print("-" * 60)

    # --- 2. RSA-OAEP ENCRYPTION DEMO ---
    print("PHASE 1: CONFIDENTIALITY (RSA-OAEP)")
    secret_text = "The launch codes are 0000-1111."
    print(f"[*] Original Message: {secret_text}")

    # Encryption
    print("[*] Encrypting with Public Key...")
    # Use byte_len to ensure the padded block matches the modulus size
    padded_enc = oaep_pad(secret_text.encode(), byte_len)
    cipher_int = pow(int.from_bytes(padded_enc, 'big'), e, n)
    print(f"[+] Ciphertext: {hex(cipher_int)[:50]}...")

    # Decryption
    print("[*] Decrypting with Private Key...")
    dec_int = pow(cipher_int, d, n)
    # Ensure the integer is converted back to the exact block size
    dec_bytes = dec_int.to_bytes(byte_len, 'big')
    recovered_text = oaep_unpad(dec_bytes, byte_len).decode()
    print(f"[+] Recovered: {recovered_text}")
    print("-" * 60)

    # --- 3. RSA-PSS SIGNATURE & TAMPER DEMO ---
    print("PHASE 2: AUTHENTICITY & INTEGRITY (RSA-PSS)")
    original_doc = "I authorize payment of $10.00 to Thomas."
    print(f"[*] Document: {original_doc}")

    # Sign (Private Key)
    print("[*] Signing with Private Key...")
    em_sign = pss_encode(original_doc.encode(), byte_len)
    sig_int = pow(int.from_bytes(em_sign, 'big'), d, n)
    
    # FIX: Use byte_len to prevent OverflowError
    signature = sig_int.to_bytes(byte_len, 'big')
    print("[+] Signature created.")

    # Tamper Test Simulation
    tampered_doc = "I authorize payment of $10,000 to Thomas."
    print(f"\n[!] ALERT: Attacker modified document to: {tampered_doc}")

    # Verify (Public Key)
    print("[*] Verifying Signature against tampered document...")
    # Reverse the RSA math: em = s^e mod n
    s_int = int.from_bytes(signature, 'big')
    recovered_em_int = pow(s_int, e, n)
    recovered_em = recovered_em_int.to_bytes(byte_len, 'big')
    
    # Check the PSS structure against the tampered text
    is_valid = pss_verify(tampered_doc.encode(), recovered_em, byte_len)
    
    if not is_valid:
        print("[SUCCESS] The signature REJECTED the tampered document!")
        print("[INFO] Integrity check failed as expected.")
    else:
        print("[ERROR] The signature was bypassable. Check logic.")
    print("=" * 60)

if __name__ == "__main__":
    run_demonstration()