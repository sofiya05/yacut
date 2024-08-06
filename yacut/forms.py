from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from yacut.constants import MAX_LENGTH, MIN_LENGTH, SHORT_MAX_LENGTH


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(
            DataRequired(message='Обязательное поле!'),
            Length(MIN_LENGTH, MAX_LENGTH),
        ),
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=(Optional(), Length(MIN_LENGTH, SHORT_MAX_LENGTH)),
    )
    submit = SubmitField('Создать')
