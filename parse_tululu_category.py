import argparse
import json
import os
import time

import requests
from bs4 import BeautifulSoup

from parse_tululu import check_for_redirect, parse_book_page, download_txt, \
    download_image


def get_last_page():
    scifi_catalog_url = 'https://tululu.org/l55/1/'
    response = requests.get(scifi_catalog_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    selector = "p.center a.npage[href]"
    pages = [page.text for page in soup.select(selector)]
    last_page = int(pages[-1])

    return last_page


if __name__ == '__main__':
    last_page = get_last_page() + 1
    current_directory = os.getcwd()
    parser = argparse.ArgumentParser(
        description='This program allows to download books'
    )
    parser.add_argument('--start_page', help='Enter the id of the first page',
                        default=1, type=int)
    parser.add_argument('--end_page', help='Enter the id of the last page',
                        default=last_page, type=int)
    parser.add_argument(
        '--dest_folder',
        help='Enter the directory for text, images, json to be stored in',
        default=current_directory,
        type=str
    )
    parser.add_argument('--skip_imgs', help='Skips images downloading',
                        default=False, action='store_const', const=True)
    parser.add_argument('--skip_txt', help='Skips txt downloading',
                        default=False, action='store_const', const=True)
    args = parser.parse_args()
    os.chdir(args.dest_folder)

    for page_num in range(args.start_page, args.end_page):
        scifi_catalog_url = f'https://tululu.org/l55/{page_num}'
        response = requests.get(scifi_catalog_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        selector = "table.d_book a[href^='/b']"
        books_ids = [a['href'] for a in soup.select(selector)]
        print(books_ids)
        books_ids = [
            int(book_id.replace('b', '').strip('/')) for book_id in books_ids
        ]

        folder_for_books = 'books'
        folder_for_images = 'images'
        downloaded_books = []
        for book_id in books_ids:
            txt_url = f'https://tululu.org/txt.php'
            params = {'id': book_id}
            book_url = f'https://tululu.org/b{book_id}/'
            reconnection_tries = 0
            while True:
                try:
                    book_response = requests.get(book_url)
                    book_response.raise_for_status()
                    check_for_redirect(book_response)
                    book = parse_book_page(book_response, book_id)
                    downloaded_books.append(book)

                    if not args.skip_txt:
                        download_txt(
                            txt_url,
                            book['title'],
                            folder_for_books,
                            params
                        )
                    if not args.skip_imgs:
                        download_image(
                            book['image_url'],
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

        downloaded_books_json = json.dumps(
            downloaded_books,
            ensure_ascii=False
        )

        with open("downloaded_books.json", "w") as file:
            file.write(downloaded_books_json)
