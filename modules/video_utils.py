import subprocess
import logging
import urllib.request
import shutil
import os
from pathlib import Path

logger = logging.getLogger(__name__)

YT_DLP_PATH = str(
    Path(__file__).resolve().parent.parent / ".dependencies" / "yt-dlp" / "yt-dlp.exe"
)
FFMPEG_PATH = str(
    Path(__file__).resolve().parent.parent / ".dependencies" / "ffmpeg" / "ffmpeg.exe"
)


def download_vod(
    vod_id: str, output_path: str, concurrent_fragments: int = 10, quality: str = "best"
) -> None:
    """
    Download a Twitch VOD via yt-dlp, optionally with multiple fragments
    and a specific format/quality.

    :param vod_id:            The numeric/string ID of the VOD (e.g. "2388768765").
    :param output_path:       Where to save the .mp4 file.
    :param concurrent_fragments:
                              How many HLS fragments to download simultaneously.
                              Higher = potentially faster, but can cause instability if too high.
    :param quality:           The quality preset. "best" tries the highest quality,
                              or you could specify something like "best[height<=720]"
                              for a 720p cap, which often downloads faster.
    """

    url = f"https://www.twitch.tv/videos/{vod_id}"

    cmd = [
        YT_DLP_PATH,
        url,
        "-o",
        output_path,
        "--format",
        quality,
        "--concurrent-fragments",
        str(concurrent_fragments),
        "--ffmpeg-location",
        FFMPEG_PATH,
    ]

    logger.info(f"Running command: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
        logger.info(f"Download of VOD {vod_id} complete.")
    except FileNotFoundError as fnf_err:
        logger.error(
            f"Could not find 'yt-dlp' executable at '{YT_DLP_PATH}'. "
            f"Ensure it's installed and the path is correct.\n{fnf_err}"
        )
        raise
    except subprocess.CalledProcessError as cpe:
        logger.error(f"yt-dlp failed to download VOD {vod_id}: {cpe}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error when downloading VOD {vod_id}: {e}")
        raise


def download_thumbnail(thumbnail_url: str, output_path: str) -> None:
    """
    Fetch a thumbnail image from the provided URL and save it locally.

    :param thumbnail_url:  Direct URL to the Twitch VOD's thumbnail image.
    :param output_path:    The local file path to which to save the image.
    """
    logger.info(
        f"Attempting to download thumbnail from {thumbnail_url} to {output_path}"
    )
    try:
        with urllib.request.urlopen(thumbnail_url) as response, open(
            output_path, "wb"
        ) as out_file:
            shutil.copyfileobj(response, out_file)
        logger.info(f"Thumbnail saved to {output_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to download thumbnail: {e}")
