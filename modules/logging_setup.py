import logging
import os
from pathlib import Path


def get_logger(script_name: str) -> logging.Logger:
    logs_dir = Path("D:/Archiver/archiver.scripts/twitch_archiver/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / f"{script_name}.log"

    logger = logging.getLogger(script_name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
