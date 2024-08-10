from http import HTTPStatus

from flask import abort, redirect, render_template, url_for

from yacut import app
from yacut.constants import REDIRECT_URL_FUNC
from yacut.forms import URLForm
from yacut.models import URLMap


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = URLMap.save_short_url(
        form.original_link.data, form.custom_id.data
    ).short
    return render_template(
        'index.html',
        form=form,
        short=short,
        short_url=url_for(REDIRECT_URL_FUNC, url=short, _external=True),
    )


@app.route('/<string:url>')
def redirect_url(url):
    short = URLMap.find_original_url(url)
    if not short:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(short.original)


@app.route('/api/docs/')
def redoc():
    return render_template('redoc.html')
