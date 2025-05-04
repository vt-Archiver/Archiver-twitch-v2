import time
import subprocess
import logging
from modules.config_utils import load_config

logger = logging.getLogger(__name__)


def main():
    config = load_config()
    channels_to_check = config.get("channels", [])
    interval = config.get("vod_check_interval_minutes", 15)

    while True:
        for channel in channels_to_check:
            # subprocess.run(["python", "download_vods.py", "--channel", channel, "--vod-id", "..."])
            pass

        logger.info(
            f"Done checking VODs for all channels. Sleeping {interval} minutes..."
        )
        time.sleep(interval * 60)


if __name__ == "__main__":
    main()
