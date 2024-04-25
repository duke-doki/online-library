# Парсер книг с сайта tululu.org

[Пример сайта.](https://duke-doki.github.io/online-library/)

Этот проект позволяет скачивать книги с сайта [tululu.org](https://tululu.org/).

### Как установить

Python3 должен быть установлен. 
Используйте `pip` (или `pip3`, если есть конфликт с Python2), чтобы установить
необходимые библиотеки:
```bash
pip install -r requirements.txt
```

### Аргументы

Чтобы скачать книги, запустите:
```
python parse_tululu.py [-h] start_id end_id
```

Чтобы скачать книги по научной фантастике, запустите:
```
python parse_tululu_category.py [-h] [--start_page START_PAGE] [--end_page END_PAGE] [--dest_folder DEST_FOLDER] [--skip_imgs] [--skip_txt]
```
Используйте `[-h]` для получения информации об аргументах.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).