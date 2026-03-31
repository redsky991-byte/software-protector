"""
Encryption helpers — XOR + base64 for trial / license data files.

The same logic is embedded verbatim inside the generated protection templates
so that protected applications are self-contained and require no extra imports.
"""
import base64
import hashlib
import json

# Key derived from a project-specific secret
_SECRET = b"MaxTechFix_SoftwareProtector_2024_ZulfiqarAli"
_KEY = hashlib.sha256(_SECRET).digest()


def _xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def encrypt_data(data: dict) -> str:
    """Encrypt a dict to a URL-safe base64 string."""
    plaintext = json.dumps(data).encode("utf-8")
    return base64.urlsafe_b64encode(_xor_bytes(plaintext, _KEY)).decode()


def decrypt_data(encrypted_str: str) -> dict:
    """Decrypt a string produced by encrypt_data back to a dict."""
    try:
        raw = base64.urlsafe_b64decode(encrypted_str.encode())
        return json.loads(_xor_bytes(raw, _KEY).decode("utf-8"))
    except Exception:
        return {}
