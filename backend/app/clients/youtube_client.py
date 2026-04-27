import os
import requests
from app.exceptions import ExternalAPIError

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def fetch_youtube_videos(query: str, max_results: int = 5) -> list[dict]:
    """
    Search YouTube for videos related to a location query.
    Returns a list of simplified video objects.
    """
    if not YOUTUBE_API_KEY:
        raise ExternalAPIError("YOUTUBE_API_KEY is not set.")

    try:
        response = requests.get(
            YOUTUBE_SEARCH_URL,
            params={
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "key": YOUTUBE_API_KEY,
            },
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
    except requests.Timeout:
        raise ExternalAPIError("YouTube API request timed out.")
    except requests.HTTPError as e:
        raise ExternalAPIError(f"YouTube API error: {e.response.status_code}")
    except requests.RequestException as e:
        raise ExternalAPIError(f"YouTube request failed: {str(e)}")

    videos = []
    for item in data.get("items", []):
        video_id = item["id"].get("videoId")
        snippet = item.get("snippet", {})
        if video_id:
            videos.append(
                {
                    "video_id": video_id,
                    "title": snippet.get("title"),
                    "channel": snippet.get("channelTitle"),
                    "thumbnail": snippet.get("thumbnails", {})
                    .get("medium", {})
                    .get("url"),
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                }
            )

    return videos
