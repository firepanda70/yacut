# Сервис создания коротких ссылок
## Описание 

Сервис позволяет пользователям добавлять для любых ссылок в интернете 
собственную короткую ссылку на платформе, которая будет возвращать редирект на 
желаемую страницу

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Добавить переменные среды в файл .env в корневой каталог:
```
FLASK_APP=yacut
FLASK_ENV=development # или production
```

## Использование

Пользователь вставляет в поле ссылку, предлагает собственный вариант короткой и нажимает кнопку создать.

![Appearance example](examples/generated_link_example.png?raw=true "Appearance example")