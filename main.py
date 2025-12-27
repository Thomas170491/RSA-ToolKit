
from utils.rsa_math import generate_rsa_keys 

def main():
    try:
        public, private = generate_rsa_keys(1024)
        
        print("\n" + "="*50)
        print("RSA KEY GENERATION SUCCESSFUL")
        print("="*50)
        print(f"Public Key (e, n): \ne: {public[0]} \nn: {hex(public[1])[:60]}...")
        print("-" * 50)
        print(f"Private Key (d, n): \nd: {hex(private[0])[:60]}...")
        print("="*50)
        
        # Simple proof of concept: Encryption/Decryption
        message = 123456789
        cipher = pow(message, public[0], public[1])
        decrypted = pow(cipher, private[0], private[1])
        
        print(f"\nVerifying math: Original {message} -> Decrypted {decrypted}")
        if message == decrypted:
            print("[STATUS] RSA Math Verified: Success!")

    except Exception as error:
        print(f"[ERROR] {error}")

if __name__ == "__main__":
    main()
                
