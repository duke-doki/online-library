# Онлайн-библиотека книг с сайта tululu.org



Этот проект позволяет развернуть свой сайт с книгами, 
а также скачивать книги с сайта [tululu.org](https://tululu.org/).

### Как установить

Python3 должен быть установлен. 
Используйте `pip` (или `pip3`, если есть конфликт с Python2), чтобы установить
необходимые библиотеки:
```bash
pip install -r requirements.txt
```

### Переменные окружения

- BOOKS

1. Положите `.env` в корневую папку проекта.
2. `.env` должен содержать данные без кавычек.

Например, если вывести данные `.env`, вы увидите:

```bash
$ cat .env
BOOKS=downloaded_books
```



## Сайт

Для локального запуска сайта запустите:
```bash
python render_website.py
```
Сайт будет доступен по этой ссылке: http://127.0.0.1:5500.
Также, сайт можно развернуть с помощью [GitHub Pages](https://pages.github.com/). 
Вот [Пример сайта](https://duke-doki.github.io/online-library/).

## Парсер

### Аргументы

Чтобы скачать книги, запустите:
```bash
python parser/parse_tululu.py [-h] start_id end_id
```

Чтобы скачать книги по научной фантастике, запустите:
```bash
python parser/parse_tululu_category.py [-h] [--start_page START_PAGE] [--end_page END_PAGE] [--dest_folder DEST_FOLDER] [--skip_imgs] [--skip_txt]
```
Используйте `[-h]` для получения информации об аргументах.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).