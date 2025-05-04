import argparse
import os
import sys
from pathlib import Path

from modules import api_utils
from modules import video_utils
from modules import db_utils
from modules import file_utils
from modules.logging_setup import get_logger

logger = get_logger("download_vods")


def main():
    parser = argparse.ArgumentParser(
        description="Download a single VOD from Twitch using yt-dlp."
    )
    parser.add_argument("--channel", required=True, help="Twitch channel name")
    parser.add_argument("--vod-id", required=True, help="Twitch VOD ID")
    parser.add_argument(
        "--output-base",
        default="D:/Archiver/persons",
        help="Base directory where VOD folders are stored.",
    )
    args = parser.parse_args()

    channel_name = args.channel
    vod_id = args.vod_id
    base_output = Path(args.output_base)

    try:
        vod_data = api_utils.get_vod_info(vod_id)
    except Exception as e:
        logger.error(f"Failed to fetch VOD info from Twitch: {e}")
        sys.exit(1)

    session_folder_name = f"{vod_data.get('created_at', 'unknown')}_{vod_id}".replace(
        ":", "-"
    )
    vod_folder = base_output / channel_name / "twitch" / "vods" / session_folder_name

    videos_folder = vod_folder / "videos"
    thumbnails_folder = vod_folder / "thumbnails"
    events_db_path = vod_folder / "events.sqlite"
    chat_db_path = vod_folder / "chat.vod.sqlite"
    metadata_json_path = vod_folder / "metadata.json"

    videos_folder.mkdir(parents=True, exist_ok=True)
    thumbnails_folder.mkdir(parents=True, exist_ok=True)

    vod_filepath = videos_folder / "vod.mp4"
    try:
        video_utils.download_vod(vod_id=vod_id, output_path=str(vod_filepath))
        logger.info(f"Successfully downloaded VOD to {vod_filepath}")
    except Exception as e:
        logger.error(f"Failed to download VOD {vod_id}: {e}")
        sys.exit(1)

    metadata = {
        "stream_id": None,
        "vod_id": vod_id,
        "title": vod_data.get("title"),
        "created_at": vod_data.get("created_at"),
        "thumbnail_url": vod_data.get("thumbnail_url"),
        "downloaded_at": file_utils.get_utc_now_str(),
        "twitch_duration": vod_data.get("duration_seconds", 0),
        "start_time": vod_data.get("start_time"),
        "end_time": vod_data.get("end_time"),
    }

    file_utils.write_json(metadata_json_path, metadata)
    logger.info(f"Wrote metadata to {metadata_json_path}")

    try:
        if metadata["thumbnail_url"]:
            thumbnail_path = thumbnails_folder / "vod_thumb.jpg"
            video_utils.download_thumbnail(metadata["thumbnail_url"], thumbnail_path)
            logger.info(f"Downloaded thumbnail: {thumbnail_path}")
    except Exception as e:
        logger.warning(f"Could not download thumbnail: {e}")

    main_db_path = Path("D:/Archiver/metadata/database.sqlite")
    try:
        db_utils.insert_vod_record(
            db_path=main_db_path,
            vod_id=vod_id,
            stream_id=None,
            channel_name=channel_name,
            folder_name=str(session_folder_name),
            vod_original_title=metadata["title"],
            created_at=metadata["created_at"],
        )
        logger.info(f"Database updated for VOD {vod_id}")
    except Exception as e:
        logger.error(f"DB insert failed for VOD {vod_id}: {e}")

    logger.info("Finished download_vods.py")


if __name__ == "__main__":
    main()
