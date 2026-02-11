import re


CNIC_PATTERN = re.compile(r"^\d{5}-\d{7}-\d$")
MOBILE_PATTERN = re.compile(r"^03\d{9}$")


def validate_imei(imei: str) -> bool:
    """Validate IMEI: 15 digits + Luhn check."""
    if not imei or len(imei) != 15 or not imei.isdigit():
        return False
    total = 0
    for i, ch in enumerate(imei):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def validate_cnic(cnic: str) -> bool:
    """Validate CNIC format: XXXXX-XXXXXXX-X."""
    return bool(CNIC_PATTERN.match(cnic))


def validate_mobile(mobile: str) -> bool:
    """Validate Pakistani mobile: starts with 03, 11 digits total."""
    return bool(MOBILE_PATTERN.match(mobile))


def validate_password(password: str) -> str | None:
    """Return error message if password is invalid, None if valid."""
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return "Password must include an uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Password must include a lowercase letter"
    if not re.search(r"\d", password):
        return "Password must include a number"
    return None


def validate_username(username: str) -> str | None:
    """Return error message if username is invalid, None if valid."""
    if len(username) < 4:
        return "Username must be at least 4 characters"
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return "Username must be alphanumeric"
    return None
