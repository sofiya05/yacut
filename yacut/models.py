import random
import re
from datetime import datetime, timezone
from http import HTTPStatus

from flask import jsonify, url_for

from yacut import db
from yacut.constants import (
    AUTO_CREATED_SHORT_MAX_LENGTH,
    ORIGINAL_URL_MAX_LENGTH,
    PATTERN,
    REDIRECT_URL_FUNC,
    SHORT_MAX_LENGTH,
    SYMBOLS,
)
from yacut.error_handlers import InvalidAPIUsage

NULL_DATA_BODY_ERROR = 'Отсутствует тело запроса'
NULL_URL_FIELD_ERROR = '"url" является обязательным полем!'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_MAX_LENGTH))
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_URL_FUNC, short=self.short, _external=True
            ),
        )

    @staticmethod
    def create_unique_short():
        short = ''.join(
            random.choices(SYMBOLS, k=AUTO_CREATED_SHORT_MAX_LENGTH)
        )
        return short

    # в константах избавляемся от смешивания валидаций а тут добавляем?
    @staticmethod
    def save_or_create_short(original, short: None):
        if not short:
            short = URLMap.create_unique_short()

        urlmap = URLMap(original=original, short=short)
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @staticmethod
    def find_URLMap_model(short):
        return URLMap.query.filter_by(short=short).first()

    # видимо принципом KISS в этом простом проекте руководствоваться
    # не приходится. Или может в ревью я смогу получить логическое
    # объяснение создания микро-ОРМ в проекте, где всего пара
    # методов? Усложнять ради усложнения можно до бесконечности

    @staticmethod
    def save_or_create_short_url_api(data):
        if not data:
            raise InvalidAPIUsage(NULL_DATA_BODY_ERROR)

        if 'url' not in data or not data['url']:
            raise InvalidAPIUsage(NULL_URL_FIELD_ERROR)

        if 'custom_id' not in data or not data['custom_id']:
            data['custom_id'] = URLMap.create_unique_short()

        short = data['custom_id']

        if len(short) > SHORT_MAX_LENGTH or not re.match(PATTERN, short):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        if URLMap.find_URLMap_model(short):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        try:
            return (
                jsonify(
                    URLMap.save_or_create_short(
                        original=data['url'], short=data['custom_id']
                    ).to_dict()
                ),
                HTTPStatus.CREATED,
            )
        except Exception as error:
            return (jsonify({'error': error}), HTTPStatus.BAD_REQUEST)
