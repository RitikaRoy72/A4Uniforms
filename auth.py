"""
auth.py — Cadet authentication helpers.

Passwords are stored in data/cadet_passwords.json as:
{
  "roy,ritika": {
      "email": "rr837@cornell.edu",
      "password_hash": "<werkzeug hash>",
      "reset_token": "<hex token or null>",
      "reset_expires": "<ISO timestamp or null>"
  },
  ...
}

The key is the cadet name exactly as it appears in the Excel file,
lowercased (e.g. "roy,ritika").
"""

import json
import os
import secrets
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash, check_password_hash

PASSWORDS_FILE = "data/cadet_passwords.json"
RESET_TOKEN_TTL_MINUTES = 30


# ── Low-level file I/O ────────────────────────────────────────────────────────

def _load() -> dict:
    if not os.path.exists(PASSWORDS_FILE):
        return {}
    with open(PASSWORDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict):
    os.makedirs(os.path.dirname(PASSWORDS_FILE), exist_ok=True)
    with open(PASSWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _key(name: str) -> str:
    """Normalise Excel name like 'Roy,Ritika' → 'roy,ritika'."""
    return name.strip().lower()


# ── Public API ────────────────────────────────────────────────────────────────

def cadet_exists(name: str) -> bool:
    return _key(name) in _load()


def is_registered(name: str) -> bool:
    """True if the cadet has already set a password."""
    data = _load()
    entry = data.get(_key(name))
    return bool(entry and entry.get("password_hash"))


def register(name: str, email: str, password: str) -> bool:
    """
    First-time registration. Returns False if already registered.
    The caller must have already verified that `name` exists in the Excel data.
    """
    data = _load()
    k = _key(name)
    if data.get(k, {}).get("password_hash"):
        return False  # already registered
    data[k] = {
        "email": email.strip().lower(),
        "password_hash": generate_password_hash(password),
        "reset_token": None,
        "reset_expires": None,
    }
    _save(data)
    return True


def verify(name: str, password: str) -> bool:
    data = _load()
    entry = data.get(_key(name))
    if not entry or not entry.get("password_hash"):
        return False
    return check_password_hash(entry["password_hash"], password)


def get_email(name: str) -> str | None:
    entry = _load().get(_key(name))
    return entry["email"] if entry else None


def find_name_by_email(email: str) -> str | None:
    """Return the raw-key (lowercased name) matching an email, or None."""
    for key, entry in _load().items():
        if entry.get("email", "").lower() == email.strip().lower():
            return key
    return None


# ── Password reset ────────────────────────────────────────────────────────────

def create_reset_token(name: str) -> str | None:
    """Generate and store a reset token. Returns the token or None if unknown."""
    data = _load()
    k = _key(name)
    if k not in data:
        return None
    token = secrets.token_urlsafe(32)
    expires = (datetime.utcnow() + timedelta(minutes=RESET_TOKEN_TTL_MINUTES)).isoformat()
    data[k]["reset_token"] = token
    data[k]["reset_expires"] = expires
    _save(data)
    return token


def validate_reset_token(token: str) -> str | None:
    """Return the cadet name key if token is valid and not expired, else None."""
    for key, entry in _load().items():
        if entry.get("reset_token") == token:
            expires = entry.get("reset_expires")
            if expires and datetime.utcnow() < datetime.fromisoformat(expires):
                return key
    return None


def apply_reset(token: str, new_password: str) -> bool:
    """Set a new password using a valid reset token. Returns True on success."""
    data = _load()
    key = validate_reset_token(token)
    if not key:
        return False
    data[key]["password_hash"] = generate_password_hash(new_password)
    data[key]["reset_token"] = None
    data[key]["reset_expires"] = None
    _save(data)
    return True


# ── Role management ───────────────────────────────────────────────────────────

def get_role(name: str) -> str:
    """
    Return the role for a registered cadet.
    Possible values: 'cadet' (default) or 'subadmin'.
    Returns 'cadet' if the entry doesn't exist or has no role set.
    """
    entry = _load().get(_key(name))
    if not entry:
        return "cadet"
    return entry.get("role", "cadet")


def set_role(name: str, role: str) -> bool:
    """
    Set the role for a registered cadet. role must be 'cadet' or 'subadmin'.
    Returns False if the cadet is not found.
    """
    if role not in ("cadet", "subadmin"):
        raise ValueError(f"Invalid role: {role!r}. Must be 'cadet' or 'subadmin'.")
    data = _load()
    k = _key(name)
    if k not in data:
        return False
    data[k]["role"] = role
    _save(data)
    return True