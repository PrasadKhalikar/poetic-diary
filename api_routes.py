from flask import Blueprint, jsonify, request
import requests

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/synonyms', methods=['GET'])
def get_synonyms():
    word = request.args.get('word')
    if not word:
        return jsonify({"error": "No word provided"}), 400
    response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch synonyms"}), 500

    synonyms = [item['word'] for item in response.json()]
    return jsonify({"word": word, "synonyms": synonyms})