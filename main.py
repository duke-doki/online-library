import requests
from pathlib import Path


Path('books').mkdir(exist_ok=True)

for book in range(10):
    url = f'https://tululu.org/txt.php?id={32168 + book}'
    response = requests.get(url)
    response.raise_for_status()
    with open(f'books/book{book}', 'w') as file:
        file.write(response.text)
