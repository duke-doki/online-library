import argparse
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history and response.url == 'https://tululu.org/':
        raise requests.HTTPError


def download_txt(url, filename, folder, params):
    Path(f'{folder}').mkdir(exist_ok=True)
    response = requests.get(url, params=params)
    response.raise_for_status()
    filename = sanitize_filename(filename)
    with open(f'{folder}/{filename}.txt', 'w') as file:
        file.write(response.text)

    return os.path.join(folder, f'{filename}.txt')


def download_image(url, filename, folder):
    Path(f'{folder}').mkdir(exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    filename = sanitize_filename(filename)
    with open(f'{folder}/{filename}', 'wb') as file:
        file.write(response.content)

    return os.path.join(folder, f'{filename}.txt')


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('h1')
    book = title_tag.text.split('::')
    title = f'{book_id}. {book[0].strip()}'
    author = book[1].strip()

    image = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin('https://tululu.org/', image)
    img_path = urlparse(image_url).path
    img_name = img_path.split('/')[-1]

    posts = soup.find_all(class_='texts')
    all_comments = []
    for post in posts:
        comment = post.find('span')
        all_comments.append(comment.text)

    genres = soup.find('span', class_='d_book').find_all('a')
    all_genres = []
    for genre in genres:
        all_genres.append(genre.text)

    book_info = {
        'title': title,
        'author': author,
        'image_url': image_url,
        'img_name': img_name,
        'comments': all_comments,
        'genres': all_genres
    }

    return book_info


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This program allows to download books'
    )
    parser.add_argument('start_id', help='Enter the id of the first book',
                        default=1, type=int)
    parser.add_argument('end_id', help='Enter the id of the last book',
                        default=2, type=int)
    args = parser.parse_args()

    folder_for_books = 'books'
    folder_for_images = 'images'
    for book_id in range(args.start_id, args.end_id+1):
        url_txt = f'https://tululu.org/txt.php'
        params = {'id': book_id}
        url_book = f'https://tululu.org/b{book_id}/'
        response_book = requests.get(url_book)
        response_book.raise_for_status()
        response_txt = requests.get(url_txt, params=params)
        response_txt.raise_for_status()
        try:
            check_for_redirect(response_book)
            check_for_redirect(response_txt)
        except requests.HTTPError:
            continue
        else:
            book_info = parse_book_page(response_book)

            download_txt(url_txt,
                         book_info['title'],
                         folder_for_books,
                         params
                         )
            download_image(book_info['image_url'],
                           book_info['img_name'],
                           folder_for_images
                           )
