import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from parse_tululu import check_for_redirect, parse_book_page, download_txt, \
    download_image



for page_num in range(1, 5):
    scifi_catalog_url = f'https://tululu.org/l55/{page_num}'
    response = requests.get(scifi_catalog_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.find_all('table', class_='d_book')
    books_ids = [book.find('a')['href'] for book in books]
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

                download_txt(
                    txt_url,
                    book['title'],
                    folder_for_books,
                    params
                )
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
