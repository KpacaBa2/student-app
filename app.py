"""Student & Course API application module."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Return root welcome message."""
    return "Student Information System", 200


@app.route("/courses", methods=["GET"])
def get_courses():
    """Return list of available courses."""
    return jsonify({
        "courses": [
            "DevOps Engineering",
            "Information Security",
            "Database Systems",
        ]
    }), 200


@app.route("/health", methods=["GET"])
def health_check():
    """Return health check status."""
    return jsonify({"status": "ok"}), 200


@app.route("/calculate-gpa", methods=["POST"])
def calculate_gpa():
    """Calculate and return average GPA from grades list."""
    data = request.get_json(silent=True)
    if not data or "grades" not in data:
        return jsonify({"error": "Invalid grades"}), 400

    grades = data["grades"]
    if not isinstance(grades, list) or len(grades) == 0:
        return jsonify({"error": "Invalid grades"}), 400

    if not all(
        isinstance(g, (int, float)) and not isinstance(g, bool)
        for g in grades
    ):
        return jsonify({"error": "Invalid grades"}), 400

    gpa = round(sum(grades) / len(grades), 2)
    return jsonify({"gpa": gpa}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
