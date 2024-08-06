from datetime import UTC, datetime

from flask import url_for

from yacut import db
from yacut.constants import MAX_LENGTH, SHORT_MAX_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH))
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now(UTC))

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_url', url=self.short, _external=True),
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])
