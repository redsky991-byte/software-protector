"""
Trial Manager — tracks install date and remaining trial days.
"""
import datetime
import os
from pathlib import Path

from .encryption import encrypt_data, decrypt_data
from .hardware_id import get_hardware_id
from .license_manager import validate_license_key

TRIAL_DAYS = 15
_DATA_DIR = Path.home() / ".sp_data"
_TRIAL_FILE = _DATA_DIR / "protector.tr"
_LICENSE_FILE = _DATA_DIR / "protector.lic"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _read_file(path: Path) -> dict:
    if path.exists():
        try:
            return decrypt_data(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _write_file(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(encrypt_data(data), encoding="utf-8")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_trial_info() -> dict:
    """Return a dict with trial/license status for the *protector* application itself."""
    hwid = get_hardware_id()

    # Check license first
    lic = _read_file(_LICENSE_FILE)
    if lic.get("email") and lic.get("key"):
        if validate_license_key(lic["email"], hwid, lic["key"]):
            return {
                "is_licensed": True,
                "email": lic["email"],
                "days_left": None,
                "days_used": None,
                "install_date": None,
                "is_expired": False,
            }

    # Check / initialise trial
    trial = _read_file(_TRIAL_FILE)
    if not trial.get("install_date"):
        trial = {"install_date": datetime.datetime.now().isoformat()}
        _write_file(_TRIAL_FILE, trial)

    install_dt = datetime.datetime.fromisoformat(trial["install_date"])
    days_used = (datetime.datetime.now() - install_dt).days
    days_left = max(0, TRIAL_DAYS - days_used)

    return {
        "is_licensed": False,
        "email": "",
        "days_left": days_left,
        "days_used": days_used,
        "install_date": install_dt,
        "is_expired": days_left == 0,
    }


def activate_license(email: str, key: str) -> bool:
    """Persist a valid license.  Returns True on success."""
    hwid = get_hardware_id()
    if validate_license_key(email, hwid, key):
        _write_file(_LICENSE_FILE, {"email": email, "key": key})
        return True
    return False
