import csv
import io
import json
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

from app.models.weather_record import WeatherRecord


def export_json(records: list[WeatherRecord]) -> str:
    return json.dumps([r.to_dict() for r in records], indent=2)


def export_csv(records: list[WeatherRecord]) -> str:
    if not records:
        return ""

    output = io.StringIO()
    fieldnames = list(records[0].to_dict().keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for r in records:
        writer.writerow(r.to_dict())

    return output.getvalue()


def export_xml(records: list[WeatherRecord]) -> str:
    root = Element("weather_records")

    for r in records:
        record_el = SubElement(root, "record")
        for key, value in r.to_dict().items():
            child = SubElement(record_el, key)
            child.text = str(value) if value is not None else ""

    raw_xml = tostring(root, encoding="unicode")
    # Pretty-print
    return parseString(raw_xml).toprettyxml(indent="  ")


EXPORT_FORMATS = {
    "json": ("application/json", "records.json", export_json),
    "csv": ("text/csv", "records.csv", export_csv),
    "xml": ("application/xml", "records.xml", export_xml),"
}


def export_records(records: list[WeatherRecord], fmt: str) -> tuple[str, str, str]:
    """
    Returns (content, mimetype, filename).
    Raises ValueError for unsupported formats.
    """
    fmt = fmt.lower()
    if fmt not in EXPORT_FORMATS:
        supported = ", ".join(EXPORT_FORMATS.keys())
        raise ValueError(f"Unsupported format '{fmt}'. Supported: {supported}")

    mimetype, filename, fn = EXPORT_FORMATS[fmt]
    return fn(records), mimetype, filename
