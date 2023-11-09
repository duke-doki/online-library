import os

import requests
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup

Path('books').mkdir(exist_ok=True)


def check_for_redirect(response):
    if response.history and response.url == 'https://tululu.org/':
        raise requests.HTTPError


def download_txt(url, filename, folder):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    Path(f'{folder}').mkdir(exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    filename = sanitize_filename(filename)
    with open(f'{folder}/{filename}', 'w') as file:
        file.write(response.text)

    return os.path.join(folder, f'{filename}.txt')


for book_id in range(1, 11):
    url_txt = f'https://tululu.org/txt.php?id={book_id}'
    url_book = f'https://tululu.org/b{book_id}/'
    response = requests.get(url_book)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    book = title_tag.text.split('::')
    title = f'{book_id}. {book[0].strip()}'
    folder = 'books'
    try:
        download_txt(url_txt, title, folder)
    except requests.HTTPError:
        continue
