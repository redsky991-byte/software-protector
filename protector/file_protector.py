"""
File Protector — wraps user files with a self-contained trial/license check.

Supported file types
--------------------
  .py          → injects protection block at top → protected_<name>.py
  .exe         → creates a Python launcher wrapper → launch_<name>.py
  <any other>  → encrypts file + creates a Python launcher → launch_<stem>.py
                  alongside  <name>.spdata  (encrypted payload)
"""
import base64
import hashlib
import os
from pathlib import Path

_TEMPLATES = Path(__file__).parent.parent / "templates"


def _app_id(file_path: str) -> str:
    return hashlib.md5(os.path.basename(file_path).encode()).hexdigest()[:12]


def _load_template(name: str) -> str:
    return (_TEMPLATES / name).read_text(encoding="utf-8")


def _replace(template: str, replacements: dict) -> str:
    result = template
    for key, val in replacements.items():
        result = result.replace(f"###{key}###", str(val))
    return result


# ---------------------------------------------------------------------------
# Individual protectors
# ---------------------------------------------------------------------------

def protect_py_file(
    input_path: str, output_path: str, app_name: str, trial_days: int = 15
) -> dict:
    src = Path(input_path)
    dst = Path(output_path)
    if not src.exists():
        return {"success": False, "error": f"File not found: {src}"}

    original_code = src.read_text(encoding="utf-8", errors="replace")
    template = _load_template("protected_py_template.py")
    protected = _replace(
        template,
        {
            "APP_NAME": app_name,
            "APP_ID": _app_id(str(src)),
            "TRIAL_DAYS": trial_days,
            "ORIGINAL_CODE": original_code,
        },
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(protected, encoding="utf-8")
    return {"success": True, "output_path": str(dst)}


def protect_exe_file(
    input_path: str, output_path: str, app_name: str, trial_days: int = 15
) -> dict:
    src = Path(input_path)
    dst = Path(output_path)
    if not src.exists():
        return {"success": False, "error": f"File not found: {src}"}

    template = _load_template("protected_exe_template.py")
    exe_escaped = str(src).replace("\\", "\\\\")
    protected = _replace(
        template,
        {
            "APP_NAME": app_name,
            "APP_ID": _app_id(str(src)),
            "TRIAL_DAYS": trial_days,
            "EXE_PATH": exe_escaped,
        },
    )
    if dst.suffix.lower() != ".py":
        dst = dst.with_suffix(".py")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(protected, encoding="utf-8")
    return {"success": True, "output_path": str(dst)}


def protect_generic_file(
    input_path: str, output_dir: str, app_name: str, trial_days: int = 15
) -> dict:
    src = Path(input_path)
    out_dir = Path(output_dir)
    if not src.exists():
        return {"success": False, "error": f"File not found: {src}"}

    app_id = _app_id(str(src))
    enc_key = hashlib.sha256(app_id.encode()).digest()
    file_bytes = src.read_bytes()
    encrypted = bytes(b ^ enc_key[i % len(enc_key)] for i, b in enumerate(file_bytes))
    enc_b64 = base64.b64encode(encrypted).decode()

    out_dir.mkdir(parents=True, exist_ok=True)
    spdata_file = out_dir / f"{src.name}.spdata"
    spdata_file.write_text(enc_b64, encoding="utf-8")

    template = _load_template("protected_generic_template.py")
    protected = _replace(
        template,
        {
            "APP_NAME": app_name,
            "APP_ID": app_id,
            "TRIAL_DAYS": trial_days,
            "ENCRYPTED_FILE": str(spdata_file).replace("\\", "\\\\"),
            "ORIGINAL_FILENAME": src.name,
            "ENCRYPTION_KEY": app_id,
        },
    )
    out_py = out_dir / f"launch_{src.stem}.py"
    out_py.write_text(protected, encoding="utf-8")
    return {
        "success": True,
        "output_path": str(out_py),
        "encrypted_file": str(spdata_file),
    }


# ---------------------------------------------------------------------------
# Unified entry point
# ---------------------------------------------------------------------------

def protect_file(
    input_path: str,
    output_dir: str,
    app_name: str = None,
    trial_days: int = 15,
) -> dict:
    """Auto-detect file type and apply the appropriate protection."""
    src = Path(input_path)
    out_dir = Path(output_dir)
    if app_name is None:
        app_name = src.stem

    ext = src.suffix.lower()
    if ext == ".py":
        dst = out_dir / f"protected_{src.name}"
        return protect_py_file(str(src), str(dst), app_name, trial_days)
    elif ext == ".exe":
        dst = out_dir / f"launch_{src.stem}.py"
        return protect_exe_file(str(src), str(dst), app_name, trial_days)
    else:
        return protect_generic_file(str(src), str(out_dir), app_name, trial_days)
