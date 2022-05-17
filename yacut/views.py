from random import choices
import re
import string

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URL_map_form
from .models import URL_map
from .contants import DEFAULT_CUSTOM_LINK_LENGTH, HOST, SHORT_LINK_MAX_LENGTH, SHORT_LINK_REGEXP


def is_shortcut_valid(shortcut):
    if len(shortcut) <= SHORT_LINK_MAX_LENGTH and re.search(SHORT_LINK_REGEXP, shortcut):
        return True
    return False


def is_shortcut_exists(shortcut):
    if URL_map.query.filter_by(short=shortcut).first():
        return True
    return False


def get_unique_short_id(length=DEFAULT_CUSTOM_LINK_LENGTH):
    while True:
        short = ''.join(choices(string.ascii_letters + string.digits, k=length))
        if is_shortcut_exists(short):
            continue
        return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URL_map_form()
    if form.validate_on_submit():
        shortcut = form.custom_id.data
        if shortcut:
            if is_shortcut_exists(shortcut):
                flash(f'Имя {shortcut} уже занято!')
                return render_template('main/main.html', form=form)
        else:
            shortcut = get_unique_short_id()
        url_map = URL_map(
            original=form.original_link.data,
            short=shortcut
        )
        db.session.add(url_map)
        db.session.commit()
        sucsess_link = HOST + shortcut
        return render_template('main/main.html', form=URL_map_form(original_link=url_map.original), sucsess_link=sucsess_link)
    return render_template('main/main.html', form=form)


@app.route('/<shortcut>', methods=['GET'])
def return_full_url(shortcut):
    if re.search(SHORT_LINK_REGEXP, shortcut):
        url_map = URL_map.query.filter_by(short=shortcut).first()
        if url_map:
            return redirect(url_map.original)
    abort(404)
