from flask import Blueprint, request, jsonify

from app.clients.youtube_client import fetch_youtube_videos
from app.clients.maps_client import fetch_maps_data
from app.exceptions import ExternalAPIError

enrichment_bp = Blueprint("enrichment", __name__)


@enrichment_bp.route("/youtube")
def youtube():
    location = request.args.get("q", "").strip()
    if not location:
        return jsonify({"error": "'q' (location) parameter is required."}), 400

    try:
        videos = fetch_youtube_videos(f"{location} travel")
        return jsonify({"query": location, "videos": videos})
    except ExternalAPIError as e:
        return jsonify({"error": str(e)}), 502
    except Exception:
        return jsonify({"error": "Unexpected error fetching YouTube videos."}), 500


@enrichment_bp.route("/maps")
def maps():
    location = request.args.get("q", "").strip()
    if not location:
        return jsonify({"error": "'q' (location) parameter is required."}), 400

    try:
        data = fetch_maps_data(location)
        return jsonify(data)
    except ExternalAPIError as e:
        return jsonify({"error": str(e)}), 502
    except Exception:
        return jsonify({"error": "Unexpected error fetching map data."}), 500
