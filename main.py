import requests
from pathlib import Path


Path('books').mkdir(exist_ok=True)


def check_for_redirect(response):
    if response.history and response.url == 'https://tululu.org/':
        raise requests.HTTPError


for book_id in range(1, 11):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url)
    response.raise_for_status()
    try:
        check_for_redirect(response)
    except requests.HTTPError:
        continue
    else:
        with open(f'books/book{book_id}', 'w') as file:
            file.write(response.text)
