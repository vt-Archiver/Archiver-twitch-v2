import json
import datetime
import logging

logger = logging.getLogger(__name__)


def write_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Could not write JSON to {path}: {e}")
        raise


def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.error(f"Could not read JSON from {path}: {e}")
        raise


def get_utc_now_str():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
