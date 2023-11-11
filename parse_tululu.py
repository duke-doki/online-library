import argparse
import os
import time

from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
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
    split_tag = title_tag.text.split('::')
    title = f'{book_id}. {split_tag[0].strip()}'
    author = split_tag[1].strip()

    image = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin(response.url, image)
    img_path = urlparse(image_url).path
    img_name = img_path.split('/')[-1]

    posts = soup.find_all(class_='texts')
    all_comments = [post.find('span').text for post in posts]

    genres = soup.find('span', class_='d_book').find_all('a')
    all_genres = [genre.text for genre in genres]

    book = {
        'title': title,
        'author': author,
        'image_url': image_url,
        'img_name': img_name,
        'comments': all_comments,
        'genres': all_genres
    }

    return book


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
        txt_url = f'https://tululu.org/txt.php'
        params = {'id': book_id}
        book_url = f'https://tululu.org/b{book_id}/'
        reconnection_tries = 0
        while True:
            try:
                book_response = requests.get(book_url)
                book_response.raise_for_status()
                txt_response = requests.get(txt_url, params=params)
                txt_response.raise_for_status()
                check_for_redirect(book_response)
                check_for_redirect(txt_response)
                book = parse_book_page(book_response)

                download_txt(txt_url,
                             book['title'],
                             folder_for_books,
                             params
                             )
                download_image(book['image_url'],
                               book['img_name'],
                               folder_for_images
                               )
            except requests.exceptions.ConnectionError as e:
                print(f'At {book_id} connection error occurred: {e}')
                reconnection_tries += 1
                if reconnection_tries <= 1:
                    print('Retrying...')
                else:
                    print('Retry after 5 seconds...')
                    time.sleep(5)
            except requests.HTTPError as e:
                print(f'At {book_id} HTTP error occurred: {e}')
                break
            else:
                break


