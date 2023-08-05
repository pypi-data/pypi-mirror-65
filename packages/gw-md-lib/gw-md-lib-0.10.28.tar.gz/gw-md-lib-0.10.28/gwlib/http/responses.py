import json
from json import JSONDecodeError

from flask import jsonify

def build_json_error(error):
    return json.dumps({
        "success": False,
        "error": str(error)
    })


def _valid_response(response):
    try:
        json.loads(response)
    except JSONDecodeError:
        raise JSONDecodeError


def HTTP_BAD_REQUEST(response):
    response = build_json_error(response)
    return jsonify(response), 400


def HTTP_RESPONSE(response):
    # _valid_response(response)
    return jsonify(response), 200


def HTTP_NOT_FOUND(response):
    return jsonify(response), 404


def HTTP_CONFLICT(response):
    response = build_json_error(response)
    return jsonify(response), 405


def HTTP_SERVER_ERROR(response):
    response = build_json_error(response)
    return jsonify(response), 500









