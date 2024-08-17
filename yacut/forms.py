from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    ValidationError,
)

from yacut.constants import (
    CUSTOM_ID_LABEL,
    LENGTH_SHORT_URL_ERROR,
    ORIGINAL_LINK_LABEL,
    ORIGINAL_LINK_REQUIRED_MESSAGE,
    ORIGINAL_URL_MAX_LENGTH,
    PATTERN,
    SHORT_MAX_LENGTH,
    SUBMIT_BUTTON_LABEL,
    SYMBOLS_ERROR_MESSAGE,
    UNIQUE_LINK_ERROR_MESSAGE,
)
from yacut.models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=(
            DataRequired(message=ORIGINAL_LINK_REQUIRED_MESSAGE),
            Length(max=ORIGINAL_URL_MAX_LENGTH),
        ),
    )
    custom_id = URLField(
        CUSTOM_ID_LABEL,
        validators=(
            Optional(),
            Length(max=SHORT_MAX_LENGTH, message=LENGTH_SHORT_URL_ERROR),
            Regexp(PATTERN, message=SYMBOLS_ERROR_MESSAGE),
        ),
    )
    submit = SubmitField(SUBMIT_BUTTON_LABEL)

    def validate_custom_id(self, short):
        if not short:
            return
        if URLMap.find_URLMap_model(short=short.data):
            raise ValidationError(UNIQUE_LINK_ERROR_MESSAGE)
