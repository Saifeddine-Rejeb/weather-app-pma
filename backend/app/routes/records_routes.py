from flask import Blueprint, request, jsonify, Response

from app.services import records_service, export_service
from app.exceptions import GeocodingError, RecordNotFoundError, InvalidDateRangeError

records_bp = Blueprint("records", __name__, url_prefix="/records")


@records_bp.route("", methods=["POST"])
def create_record():
    data = request.get_json(silent=True) or {}

    location = data.get("location", "").strip()
    start_date = data.get("start_date", "").strip()
    end_date = data.get("end_date", "").strip()

    if not location or not start_date or not end_date:
        return (
            jsonify(
                {"error": "'location', 'start_date', and 'end_date' are all required."}
            ),
            400,
        )

    try:
        record = records_service.create_record(location, start_date, end_date)
        return jsonify(record.to_dict()), 201
    except InvalidDateRangeError as e:
        return jsonify({"error": str(e)}), 400
    except GeocodingError as e:
        return jsonify({"error": str(e)}), 422
    except Exception:
        return jsonify({"error": "Failed to create record."}), 500


@records_bp.route("", methods=["GET"])
def get_records():
    try:
        records = records_service.get_all_records()
        return jsonify([r.to_dict() for r in records])
    except Exception:
        return jsonify({"error": "Failed to fetch records."}), 500


@records_bp.route("/export", methods=["GET"])
def export_records():
    fmt = request.args.get("format", "json").strip().lower()

    try:
        records = records_service.get_all_records()
        content, mimetype, filename = export_service.export_records(records, fmt)
        return Response(
            content,
            mimetype=mimetype,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to export records."}), 500


@records_bp.route("/<int:record_id>", methods=["GET"])
def get_record(record_id):
    try:
        record = records_service.get_record_by_id(record_id)
        return jsonify(record.to_dict())
    except RecordNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Failed to fetch record."}), 500


@records_bp.route("/<int:record_id>", methods=["PUT"])
def update_record(record_id):
    data = request.get_json(silent=True) or {}

    if not data:
        return jsonify({"error": "Request body cannot be empty."}), 400

    try:
        record = records_service.update_record(record_id, data)
        return jsonify(record.to_dict())
    except RecordNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except InvalidDateRangeError as e:
        return jsonify({"error": str(e)}), 400
    except GeocodingError as e:
        return jsonify({"error": str(e)}), 422
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to update record."}), 500


@records_bp.route("/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    try:
        records_service.delete_record(record_id)
        return jsonify({"message": f"Record {record_id} deleted."})
    except RecordNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Failed to delete record."}), 500
