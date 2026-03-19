# RSA Security Toolkit

A professional, modular implementation of the RSA (Rivest–Shamir–Adleman) cryptosystem, providing both **Confidentiality** (OAEP) and **Authenticity** (PSS). Includes a practical **attack simulation** to demonstrate weaknesses in weak RSA implementations.  

This toolkit is designed for educational and portfolio purposes, demonstrating real-world cryptography concepts with a clean CLI interface.

---

## 🛠 Architecture

- **`rsa_security_toolkit.py`**: Main CLI entry point for demonstration, encryption, decryption, signing, and verification.  
- **`attack_demo.py`**: Shows how RSA can be broken with weak parameters (small primes).  
- **`utils/rsa_math.py`**: Keypair generation and core RSA math.  
- **`utils/padding.py`**: OAEP padding for secure encryption.  
- **`utils/signatures.py`**: PSS encoding for secure digital signatures.  
- **`utils/key_manager.py`**: Save/load keys and wrapper functions for encrypt/decrypt/sign/verify.  
- **Math Engine:** [Prime-Logic-MillerRabin](https://github.com/Thomas170491/Prime-Logic-MillerRabin) — cryptographically secure prime generation.  

---

## 🚀 Features

- **RSA-OAEP Encryption:** Probabilistic encryption for semantic security.  
- **RSASSA-PSS Signatures:** Digital signatures for authenticity and integrity.  
- **Tamper Detection:** Shows signature failure when a document is modified.  
- **Attack Simulation:** Demonstrates how weak RSA parameters can be exploited.  
- **CLI Interface:** Encrypt, decrypt, sign, verify directly from the terminal.  
- **Secure Randomness:** Uses Python’s `secrets` module.  
- **Miller-Rabin Primality Test:** Finds large 1024-bit primes reliably.  

---

## 🧮 Mathematical Background

See [MATHEMATICAL_BACKGROUND.md](MATHEMATICAL_BACKGROUND.md) for a detailed explanation of RSA, OAEP, PSS, key generation, and proof of correctness.  

---

## ▶️ CLI Usage

Run the CLI commands using Python:

### **1. Demo**
Show the full demonstration (encryption, decryption, signing, tamper detection):

```bash
python rsa_security_toolkit.py demo
```
### **2. Attack Simulation**
Demonstrates how RSA can be broken when weak parameters (small primes) are used. The simulation performs the following steps:

1. Attacker intercepts the public key `(e, n)`.  
2. Factors `n` into its prime components `p` and `q`.  
3. Recovers the private key `d`.  
4. Decrypts the message without authorization.  

> ⚠️ This highlights why **RSA security depends entirely on the difficulty of factoring large integers**. Small key sizes are trivially breakable.

```bash
python rsa_security_toolkit.py attack
```
### **3. Encrypt a Message**
Encrypt plaintext using the public key. The ciphertext is returned in hexadecimal.

```bash
python rsa_security_toolkit.py encrypt "hello world"
```
#### Example output

```bash
Ciphertext (hex): 0x9a45c611f130453ffb6ea20bfdf068faacf9b57963...
```

### **4. Decrypt a Message**
Decrypt a ciphertext (hexadecimal) using the private key:

```bash
python rsa_security_toolkit.py decrypt 0x9a45c611f130453ffb6ea20bfdf068faacf9b57963...
```
#### Example output

```bash
Decrypted message : hello world
```

### **5. Sign a Message**
Sign a plaintext message using the private key:

```bash
python rsa_security_toolkit.py sign "Authorize payment $10"
```

The signature is returned in hexadecimal.

### **6. Verify a Signature**
Verify a signed message using the public key:

```bash
python rsa_security_toolkit.py verify "Authorize payment $10" <signature_hex>
```
The CLI will indicate whether the signature is valid or invalid.

## **6. Installation & Setup**

```markdown
## 🔧 Installation & Setup

Clone the repository along with submodules:

```bash
git clone --recursive https://github.com/Thomas170491/rsa-security-toolkit.git
cd rsa-security-toolkit
```
###⚠️ Educational use only:

- Not constant-time → vulnerable to timing attacks

- No side-channel protections

- Key generation not hardened for production

## 🌍 Real-World Applications

- **TLS / HTTPS:** RSA key exchange in secure web communication  
- **Digital Certificates:** Signing and verification in PKI  
- **Secure Email (PGP):** Encrypting and signing messages  
- **Code Signing:** Software verification for integrity  

This project demonstrates the same foundational mechanisms used in these systems.

## 📄 License

MIT License — see [LICENSE](LICENSE) file.  

You are free to use, modify, and distribute this project for educational or portfolio purposes.