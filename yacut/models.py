import random
import re
from datetime import datetime, timezone

from flask import url_for

from yacut import db
from yacut.constants import (
    MAKE_UNIQUE_URL_BACKUP_FACTOR,
    MAX_LENGTH,
    NONE_SHORT_MAX_LENGTH,
    PATTERN,
    REDIRECT_URL_FUNC,
    SHORT_MAX_LENGTH,
    SYMBOLS,
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH))
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_URL_FUNC, url=self.short, _external=True
            ),
        )

    @staticmethod
    def check_symbols(short):
        return True if re.match(PATTERN, short) else False

    @staticmethod
    def create_unique_short_url():
        for _ in range(MAKE_UNIQUE_URL_BACKUP_FACTOR):
            short = ''.join(random.choices(SYMBOLS, k=NONE_SHORT_MAX_LENGTH))
            if URLMap.query.filter_by(short=short).first():
                short = ''.join(
                    random.choices(SYMBOLS, k=NONE_SHORT_MAX_LENGTH)
                )
            else:
                break
        return short

    @staticmethod
    def save_short_url(original, short: None):
        if not short:
            short = URLMap.create_unique_short_url()

        urlmap = URLMap(original=original, short=short)
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @staticmethod
    def find_original_url(short):
        return URLMap.query.filter_by(short=short).first()
