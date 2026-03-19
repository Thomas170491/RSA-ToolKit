import pytest 
import os
import sys

sys.path.append(os.path.join(os.getcwd()))

from utils.rsa_math import generate_rsa_keys
from utils.key_manager import (
    encrypt_message,
    decrypt_message,
    sign_message,
    verify_signature
)

# Generate a small key for faster testing
@pytest.fixture
def rsa_keys():
    return generate_rsa_keys(512)  # faster than 1024 for tests


def test_encrypt_decrypt(rsa_keys):
    (d, n_priv), (e, n_pub) = rsa_keys
    assert n_pub == n_priv, "Public and private modules mismatch!"

    message = "hello world"
    cipher = encrypt_message(message ,e, n_pub)
    print(cipher)
    decrypted = decrypt_message(cipher, d, n_priv)

    assert decrypted == message


def test_sign_verify_valid(rsa_keys):
    (d, n_priv), (e, n_pub) = rsa_keys

    message = "secure message"
    signature = sign_message(message, d, n_priv)
    is_valid = verify_signature(message, signature, e, n_pub)

    assert is_valid is True


def test_sign_verify_tampered(rsa_keys):
    (d, n_priv), (e, n_pub) = rsa_keys

    message = "secure message"
    tampered = "hacked message"

    signature = sign_message(message, d, n_pub)
    is_valid = verify_signature(tampered, signature, e, n_priv)

    assert is_valid is False


def test_encrypt_randomness(rsa_keys):
    (d, n), (e, n) = rsa_keys

    message = "same message"

    cipher1 = encrypt_message(message,e, n)
    cipher2 = encrypt_message(message, e, n)

    # OAEP should produce different ciphertexts
    assert cipher1 != cipher2