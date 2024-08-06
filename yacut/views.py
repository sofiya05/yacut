from flask import abort, redirect, render_template

from yacut import app, db
from yacut.constants import SHORT_MAX_LENGTH
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.utils import check_symbols, create_unique_short_url, flash_message


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = URLForm()
    short = form.custom_id.data
    if form.validate_on_submit():
        if URLMap.query.filter_by(short=short).first():
            return flash_message(
                'Предложенный вариант короткой ссылки уже существует.', form
            )
        if short and not check_symbols(short):
            return flash_message('Допустимые символы: A-z, 0-9', form)

        if not short:
            short = create_unique_short_url()

        if len(short) > SHORT_MAX_LENGTH:
            return flash_message(
                'Длина ссылки должна быть не более 16 символов', form
            )

        urlmap = URLMap(original=form.original_link.data, short=short)
        db.session.add(urlmap)
        db.session.commit()
        return render_template('yacut.html', form=form, short_url=urlmap.short)
    return render_template('yacut.html', form=form)


@app.route('/<string:url>')
def redirect_url(url):
    short_url = URLMap.query.filter_by(short=url).first()
    if not short_url:
        abort(404)
    return redirect(short_url.original)


@app.route('/api/docs/')
def redoc():
    return render_template('redoc.html')
