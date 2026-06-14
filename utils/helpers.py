from datetime import datetime


def utc_now_iso():
    return datetime.utcnow().isoformat() + "Z"
