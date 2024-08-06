import random
from string import ascii_letters, digits

from flask import flash, render_template

from yacut.constants import NONE_SHORT_MAX_LENGTH
from yacut.models import URLMap

SYMBOLS = ascii_letters + digits


def generate_random_short_url():
    short = random.choices(SYMBOLS, k=NONE_SHORT_MAX_LENGTH)
    return ''.join(short)


def check_symbols(custom_id):
    for element in custom_id:
        if element not in SYMBOLS:
            return False
    return True


def flash_message(msg, form):
    flash(msg)
    return render_template('yacut.html', form=form)


def create_unique_short_url():
    short_url = generate_random_short_url()
    while URLMap.query.filter_by(short=short_url).first():
        short_url = generate_random_short_url()
    return short_url
