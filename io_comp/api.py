from datetime import timedelta

from flask import Flask, jsonify, request

from io_comp.repository import get_default_repository
from io_comp.service import AvailabilityFinder


app = Flask(__name__)


def _build_service() -> AvailabilityFinder:
    """
    Construct the service with the default repository.

    Keeping this in a helper makes it easy to swap implementations
    (for example, to inject a different repository in tests or to
    move from CSV to a database-backed repository).
    """
    repo = get_default_repository()
    return AvailabilityFinder(repo)


@app.get("/availability")
def get_availability():
    """
    HTTP API endpoint that exposes the availability-finding logic.

    Query parameters:
    - people: comma-separated list of people (e.g. ?people=Alice,Jack)
    - duration: meeting duration in minutes (default: 60)
    """
    people_param = request.args.get("people", "")
    duration_minutes = int(request.args.get("duration", "60"))

    people = [p.strip() for p in people_param.split(",") if p.strip()] or ["Alice", "Jack"]
    duration = timedelta(minutes=duration_minutes)

    service = _build_service()
    slots = service.find_available_slots(people, duration)

    result = [
        {
            "earliest": slot.earliest.strftime("%H:%M"),
            "latest": slot.latest.strftime("%H:%M"),
        }
        for slot in slots
    ]
    return jsonify(result)


def main():
    """
    Run the Flask development server.

    Intended as a lightweight additional feature to expose the
    scheduling logic over HTTP.
    """
    app.run(debug=True)


if __name__ == "__main__":
    main()

