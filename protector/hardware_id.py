"""
Hardware ID module — generates a unique machine fingerprint based on MAC address.
"""
import uuid
import hashlib


def get_hardware_id() -> str:
    """Return a formatted 16-char hex hardware ID derived from the MAC address."""
    mac = uuid.getnode()
    mac_hex = format(mac, "012x")
    raw = ":".join(mac_hex[i : i + 2] for i in range(0, 12, 2))
    digest = hashlib.sha256(raw.encode()).hexdigest()[:16].upper()
    return "-".join(digest[i : i + 4] for i in range(0, 16, 4))
