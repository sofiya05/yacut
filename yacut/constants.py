from string import ascii_letters, digits

ORIGINAL_URL_MAX_LENGTH = 1000
SHORT_MAX_LENGTH = 16
AUTO_CREATED_SHORT_MAX_LENGTH = 6
ORIGINAL_LINK_LABEL = 'Длинная ссылка'
ORIGINAL_LINK_REQUIRED_MESSAGE = 'Обязательное поле!'
CUSTOM_ID_LABEL = 'Ваш вариант короткой ссылки'
SUBMIT_BUTTON_LABEL = 'Создать'
SYMBOLS_ERROR_MESSAGE = 'Допустимые символы: A-z, 0-9'
UNIQUE_LINK_ERROR_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
LENGTH_SHORT_URL_ERROR = 'Длина ссылки должна быть не более 16 символов'
SYMBOLS = ascii_letters + digits
PATTERN = rf'^[{SYMBOLS}]+$'
REDIRECT_URL_FUNC = 'redirect_url'
