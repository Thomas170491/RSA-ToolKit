🔐 RSA Security Toolkit: Encryption, Signatures & Attack Simulation

A modular, industry-inspired implementation of the RSA (Rivest–Shamir–Adleman) cryptosystem, demonstrating both confidentiality (OAEP) and authenticity (PSS) — along with a practical attack simulation showing how RSA fails under weak parameters.

🛠 Architecture

This project follows a separation of concerns design. Core cryptographic primitives are modularized, and prime generation is handled via a dedicated submodule.

rsa-toolkit/
│
├── main.py                  # Secure usage demo (encryption + signatures)
├── attack_demo.py           # 🔴 Attack simulation (breaking weak RSA)
│
├── utils/
│   ├── rsa_math.py          # Key generation (e, d, n)
│   ├── padding.py           # OAEP padding implementation
│   ├── signatures.py        # PSS encoding & verification
│
└── README.md

Math Engine: https://github.com/Thomas170491/Prime-Logic-MillerRabin

Uses Miller–Rabin primality testing for generating large primes

🚀 Features

🔐 RSA-OAEP Encryption
Probabilistic encryption preventing frequency analysis

✍️ RSASSA-PSS Signatures
Secure signing ensuring integrity and non-repudiation

🧪 Tamper Detection Demo
Demonstrates how signature verification fails when data is modified

🎲 Secure Randomness
Uses Python’s secrets module for cryptographic entropy

🔍 Attack Simulation
Demonstrates how RSA can be broken when weak parameters are used

▶️ Usage
Run secure RSA demo:
python main.py
Run attack simulation:
python attack_demo.py
🔴 Breaking Weak RSA (Attack Simulation)

This project includes a practical demonstration of how RSA can fail when implemented incorrectly.

Using deliberately weak parameters (small primes), we simulate a real-world attack:

Attacker intercepts the public key (e, n)

Factors n into p and q

Reconstructs the private key d

Decrypts encrypted data

👉 This demonstrates a fundamental principle:

RSA security relies entirely on the difficulty of factoring large integers

⚠️ With small key sizes, RSA becomes trivially breakable.

🧮 Mathematical Background

RSA security is based on the Integer Factorization Problem:

Easy: Multiply large primes

Hard: Factor the result back into primes

1. Key Generation

Select two large primes p, q

Compute modulus:
n = p × q

Compute totient:
φ(n) = (p − 1)(q − 1)

Choose public exponent:
e = 65537

Compute private key:
d × e ≡ 1 mod φ(n)

2. Encryption & Decryption

Encryption:
C = M^e mod n

Decryption:
M = C^d mod n

3. Digital Signatures (RSA-PSS)

Signing:
S = EM^d mod n

Verification:
EM = S^e mod n

4. Proof of Correctness

Based on Euler’s Theorem:

M^(ed) ≡ M mod n

🛡️ Security Considerations
Why OAEP & PSS?

This implementation follows modern standards instead of insecure "textbook RSA":

Semantic Security: Random padding prevents identical ciphertexts

Malleability Protection: Tampering results in invalid output

Integrity: PSS ensures signatures fail on modification

🌍 Real-World Applications

RSA is widely used in modern systems:

🌐 TLS / HTTPS → Secure web communication

🔑 Public Key Infrastructure (PKI) → Certificates & authentication

📧 Secure Email (PGP) → Encryption and signing

💻 Code Signing → Software integrity verification

👉 This project demonstrates the same primitives used in these systems.

⚠️ Security Disclaimer

This implementation is for educational purposes only.

It is NOT secure for production use due to:

No constant-time operations → vulnerable to timing attacks

No side-channel attack protection

Simplified padding validation

No secure key storage

👉 In production, always use well-established cryptographic libraries.

📦 Installation

Clone the repository with submodules:

git clone --recursive https://github.com/Thomas170491/RSA-Key-Gen.git

📄 License

This project is open-source and available under the MIT License.