import re

from flask import jsonify, request

from . import app, db
from .contants import HOST, SHORT_LINK_REGEXP, URL_REGEXP
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id, is_shortcut_exists


@app.route('/api/id/', methods=['POST'])
def add_url_map():
    data = request.get_json()
    if data is None or '':
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not re.search(URL_REGEXP, data['url']):
        raise InvalidAPIUsage('Не верный формат ссылки в поле "url"')
    if 'custom_id' in data and data['custom_id'] not in ('', None):
        if not re.search(SHORT_LINK_REGEXP, data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        shortcut = data['custom_id']
        if is_shortcut_exists(shortcut):
            raise InvalidAPIUsage(f'Имя "{shortcut}" уже занято.')
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
    raise InvalidAPIUsage('Указанный id не найден', 404)
