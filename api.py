import importlib.util
import json
from pathlib import Path

from flask import Flask, jsonify, request


app = Flask(__name__)


def _load_correction_module():
    """
    Load the spell-correction module from Edit-Distance-Play-around/correction.py.

    The directory name is not a valid Python package name, so we load it
    via importlib from its file path.
    """
    root = Path(__file__).parent
    correction_path = root / "Edit-Distance-Play-around" / "correction.py"
    spec = importlib.util.spec_from_file_location("correction_module", correction_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_correction = _load_correction_module()


@app.route("/api/spellcheck", methods=["POST"])
def api_spellcheck():
    """
    Spell-check a single line of text.

    Request JSON:
      { "text": "some sentence to check" }

    Response JSON:
      {
        "original": "...",
        "tokenized": "...",
        "corrected": "...",
        "num_corrections": 2,
        "corrections": [
          {
            "original": "teh",
            "corrected": "the",
            "distance": 1.0,
            "alternatives": ["the", "ten", ...]
          },
          ...
        ]
      }
    """
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Field 'text' must be a non-empty string"}), 400

    result = _correction.spellcheck_text(text)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

