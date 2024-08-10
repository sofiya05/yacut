from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.constants import SHORT_MAX_LENGTH
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap


@app.route('/api/id/', methods=('POST',))
def save_short_url():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if 'custom_id' not in data or not data['custom_id']:
        data['custom_id'] = URLMap.create_unique_short_url()

    short = data['custom_id']

    if len(short) > SHORT_MAX_LENGTH or not URLMap.check_symbols(short):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if URLMap.find_original_url(short):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    return (
        jsonify(
            URLMap.save_short_url(
                original=data.get('url'), short=data.get('custom_id')
            ).to_dict()
        ),
        HTTPStatus.CREATED,
    )


@app.route('/api/id/<string:short>/', methods=('GET',))
def get_original_url(short):
    url = URLMap.find_original_url(short)
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
