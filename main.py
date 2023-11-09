import os

import requests
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlsplit


def check_for_redirect(response):
    if response.history and response.url == 'https://tululu.org/':
        raise requests.HTTPError


def download_txt(url, filename, folder):
    Path(f'{folder}').mkdir(exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    #check_for_redirect(response)
    filename = sanitize_filename(filename)
    with open(f'{folder}/{filename}.txt', 'w') as file:
        file.write(response.text)

    return os.path.join(folder, f'{filename}.txt')


def download_image(url, filename, folder):
    Path(f'{folder}').mkdir(exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    #check_for_redirect(response)
    filename = sanitize_filename(filename)
    with open(f'{folder}/{filename}', 'wb') as file:
        file.write(response.content)

    return os.path.join(folder, f'{filename}.txt')


for book_id in range(1, 11):
    url_txt = f'https://tululu.org/txt.php?id={book_id}'
    url_book = f'https://tululu.org/b{book_id}/'
    response_book = requests.get(url_book)
    response_book.raise_for_status()
    response_txt = requests.get(url_txt)
    response_txt.raise_for_status()
    try:
        check_for_redirect(response_book)
        check_for_redirect(response_txt)
    except requests.HTTPError:
        continue
    else:
        soup = BeautifulSoup(response_book.text, 'lxml')

        title_tag = soup.find('h1')
        book = title_tag.text.split('::')
        title = f'{book_id}. {book[0].strip()}'

        image = soup.find('div', class_='bookimage').find('img')['src']
        image_url = urljoin('https://tululu.org/', image)
        img_path = urlparse(image_url).path
        img_name = img_path.split('/')[-1]

        folder_for_books = 'books'
        folder_for_images = 'images'

        posts = soup.find_all(class_='texts')
        genres = soup.find('span', class_='d_book').find_all('a')
        print('Заголовок', title)

        for genre in genres:
            print(genre.text)

        print('Комментарии:')
        for post in posts:
            comment = post.find('span')
            print(comment.text)

        # download_txt(url_txt, title, folder_for_books)
        # download_image(image_url, img_name, folder_for_images)

