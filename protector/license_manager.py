"""
License Manager — HMAC-SHA256 based license key generation and validation.

A license key is bound to (email, hardware_id) so it only works on one machine.
"""
import hashlib
import hmac

_LICENSE_SECRET = "MaxTechFix_License_Secret_ZulfiqarAli_2024"


def generate_license_key(email: str, hardware_id: str) -> str:
    """Generate a license key for a given email + hardware_id pair.

    Returns a key in the format XXXX-XXXX-XXXX-XXXX.
    """
    email_clean = email.lower().strip()
    hwid_clean = hardware_id.upper().strip().replace("-", "")
    raw = f"{email_clean}:{hwid_clean}"
    sig = hmac.new(
        _LICENSE_SECRET.encode(), raw.encode(), hashlib.sha256
    ).hexdigest()
    key = sig[:16].upper()
    return "-".join(key[i : i + 4] for i in range(0, 16, 4))


def validate_license_key(email: str, hardware_id: str, key: str) -> bool:
    """Return True when key matches the expected key for email + hardware_id."""
    expected = generate_license_key(email, hardware_id)
    provided_clean = key.replace("-", "").upper()
    expected_clean = expected.replace("-", "").upper()
    return hmac.compare_digest(provided_clean, expected_clean)
