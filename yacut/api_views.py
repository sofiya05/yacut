from http import HTTPStatus

from flask import jsonify, request

from yacut import app, db
from yacut.constants import SHORT_MAX_LENGTH
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import check_symbols, create_unique_short_url


@app.route('/api/id/', methods=('POST',))
def create_url():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if 'custom_id' not in data or not data['custom_id']:
        data['custom_id'] = create_unique_short_url()

    custom_id = data['custom_id']

    if len(custom_id) > SHORT_MAX_LENGTH or not check_symbols(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(
            f'Предложенный вариант короткой ссылки уже существует.'
        )

    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
