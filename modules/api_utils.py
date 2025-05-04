import requests
import logging
import re
from .config_utils import TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN, load_config

logger = logging.getLogger(__name__)


def get_vod_info(vod_id: str) -> dict:
    url = f"https://api.twitch.tv/helix/videos?id={vod_id}"

    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}",
    }

    logger.debug(f"Requesting VOD info from Twitch at URL: {url}")
    logger.debug(
        f"Using CLIENT_ID={TWITCH_CLIENT_ID[:4]}... and token of length {len(TWITCH_ACCESS_TOKEN)}"
    )

    response = None
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred when fetching VOD {vod_id}: {http_err}")
        if response is not None:
            logger.error(f"Response Status Code: {response.status_code}")
            logger.error(f"Response Content: {response.text}")
        raise
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request failed unexpectedly for VOD {vod_id}: {req_err}")
        raise

    data = response.json().get("data", [])
    if not data:
        raise ValueError(
            f"No data returned for VOD {vod_id}. Response text: {response.text}"
        )

    vod_info = data[0]
    # Example fields from Twitch Helix for a video object:
    # {
    #   'id': '2388768765',
    #   'user_id': '...',
    #   'user_login': 'somechannel',
    #   'title': 'Example Title',
    #   'description': '',
    #   'created_at': '2023-01-01T00:00:00Z',
    #   'published_at': '2023-01-01T00:00:00Z',
    #   'url': 'https://www.twitch.tv/videos/2388768765',
    #   'thumbnail_url': '...',
    #   'viewable': 'public' or 'private',
    #   'language': 'en',
    #   'type': 'archive',
    #   'duration': '1h2m3s',
    #   ...
    # }

    duration_seconds = parse_twitch_duration(vod_info.get("duration", ""))

    result = {
        "vod_id": vod_info.get("id"),
        "user_id": vod_info.get("user_id"),
        "user_login": vod_info.get("user_login"),
        "title": vod_info.get("title"),
        "description": vod_info.get("description"),
        "created_at": vod_info.get("created_at"),
        "published_at": vod_info.get("published_at"),
        "url": vod_info.get("url"),
        "thumbnail_url": vod_info.get("thumbnail_url"),
        "duration_seconds": duration_seconds,
        "viewable": vod_info.get("viewable"),
        "type": vod_info.get("type"),
    }

    logger.debug(f"VOD Info: {result}")
    return result


def parse_twitch_duration(duration_str: str) -> int:
    if not duration_str:
        return 0

    # Example patterns:
    #  "1h2m3s" => hours=1, minutes=2, seconds=3 => total=3723
    #  "59s" => hours=0, minutes=0, seconds=59 => total=59
    #  "2h" => hours=2, minutes=0, seconds=0 => total=7200

    regex_pattern = r"^((?P<hours>\d+)h)?((?P<minutes>\d+)m)?((?P<seconds>\d+)s)?$"
    match = re.match(regex_pattern, duration_str)
    if not match:
        return 0

    hours = int(match.group("hours")) if match.group("hours") else 0
    minutes = int(match.group("minutes")) if match.group("minutes") else 0
    seconds = int(match.group("seconds")) if match.group("seconds") else 0

    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds
