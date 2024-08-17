from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap


@app.route('/api/id/', methods=('POST',))
def save_or_create_short_url():
    return URLMap.save_or_create_short_url_api(request.get_json(silent=True))


@app.route('/api/id/<string:short>/', methods=('GET',))
def get_original_url(short):
    URLMap_model = URLMap.find_URLMap_model(short)
    if not URLMap_model:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': URLMap_model.original}), HTTPStatus.OK
