from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional, URL, Regexp

from .contants import SHORT_LINK_REGEXP

CUSTOM_ID_VALIDATION_MESSAGE = ('Которткая ссылка должна:\n'
                                '- состоять из букв латинского алфавита или цифр\n'
                                '- быть длинной от 1 до 16 символов')


class URL_map_form(FlaskForm):
    original_link = URLField(
        label='Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Неверный формат ссылки')]
    )
    custom_id = StringField(
        label='Ваш вариант короткой ссылки',
        validators=[Optional(),
                    Regexp(SHORT_LINK_REGEXP,
                           message=CUSTOM_ID_VALIDATION_MESSAGE)]
    )
    submit = SubmitField(label='Создать')
