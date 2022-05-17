import re

from flask import jsonify, request

from . import app, db
from .contants import HOST, SHORT_LINK_REGEXP, URL_REGEXP
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id, is_shortcut_exists

NO_REQUEST_BODY = 'Отсутствует тело запроса'
NO_REQUIRED_FIELD = '"{field}" является обязательным полем!'
WRONG_FORMAL = 'Не верный формат ссылки в поле "{field}"'
WRONG_SHORTCUT_NAME = 'Указано недопустимое имя для короткой ссылки'
NAME_TAKEN = 'Имя "{shortcut}" уже занято.'
ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_url_map():
    data = request.get_json()
    if data is None or '':
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage(NO_REQUIRED_FIELD.format(field='url'))
    if not re.search(URL_REGEXP, data['url']):
        raise InvalidAPIUsage(WRONG_FORMAL.format(field='url'))
    if 'custom_id' in data and data['custom_id'] not in ('', None):
        if not re.search(SHORT_LINK_REGEXP, data['custom_id']):
            raise InvalidAPIUsage(WRONG_SHORTCUT_NAME)
        shortcut = data['custom_id']
        if is_shortcut_exists(shortcut):
            raise InvalidAPIUsage(NAME_TAKEN.format(shortcut=shortcut))
    else:
        shortcut = get_unique_short_id()

    url_map = URL_map(
        original=data['url'],
        short=shortcut
    )
    db.session.add(url_map)
    db.session.commit()

    return jsonify({'short_link': HOST + url_map.short, 'url': url_map.original}), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    if re.search(SHORT_LINK_REGEXP, short_id):
        url_map = URL_map.query.filter_by(short=short_id).first()
        if url_map:
            return jsonify({'url': url_map.original}), 200
    raise InvalidAPIUsage(ID_NOT_FOUND, 404)
