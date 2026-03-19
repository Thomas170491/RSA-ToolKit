import sys
import os
import argparse

# Ensure we can find our custom modules in the current directory
sys.path.append(os.path.join(os.getcwd()))

from utils.key_manager import (
    load_keys, save_keys,
    encrypt_message, decrypt_message,
    sign_message, verify_signature
)
from attack_demo import run_demonstration, run_attack

def main() :
   parser = argparse.ArgumentParser(description='RSA Security ToolKit')
   parser.add_argument(
      "action",
      choices= ["demo","attack", "encrypt", "decrypt", "sign","verify signature"]
   )
   parser.add_argument(
      "data", nargs='?', help = "Message or ciphertext (hex for decrypt/signature)"
   )
   args = parser.parse_args()

   # Load existing keys or generate new

   keys = load_keys()
   if keys :
      (d,n), (e,n) = keys
   else :
      from utils.rsa_math import generate_rsa_keys
      (d,n), (e,n) = generate_rsa_keys()
      save_keys((d,n), ((e,n)))

    # CLI actions
   if args.action == "demo":
        run_demonstration()
   elif args.action == "attack":
        run_attack()
   elif args.action == "encrypt":
        if args.data:
            print(encrypt_message(args.data, e, n))
        else:
            print("Error: Provide a message to encrypt.")
   elif args.action == "decrypt":
        if args.data:
            print(decrypt_message(args.data, d, n))
        else:
            print("Error: Provide a ciphertext to decrypt.")
   elif args.action == "sign":
        if args.data:
            print(sign_message(args.data, d, n))
        else:
            print("Error: Provide a message to sign.")
   elif args.action == "verify":
        if args.data:
            try:
                message, sig_hex = args.data.split(",", 1)
                print("Signature valid:", verify_signature(message, sig_hex, e, n))
            except ValueError:
                print("Error: Provide input as 'message,signature_hex'")
        else:
            print("Error: Provide input as 'message,signature_hex'")


if __name__ == "__main__":
   main()