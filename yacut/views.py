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
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=url_for(
                REDIRECT_URL_FUNC,
                short=URLMap.save_or_create_short(
                    form.original_link.data, form.custom_id.data
                ).short,
                _external=True,
            ),
        )
    except Exception:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/<string:short>')
def redirect_url(short):
    URLModel = URLMap.find_URLMap_model(short)
    if not URLModel:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(URLModel.original)


@app.route('/api/docs/')
def redoc():
    return render_template('redoc.html')
