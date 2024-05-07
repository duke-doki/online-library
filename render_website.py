import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def render_website():
    with open('downloaded_books.json', 'r') as file:
        books_json = file.read()
    books = json.loads(books_json)
    paged_books = list(chunked(books, 20))
    pages_num = len(paged_books)
    os.makedirs('pages', exist_ok=True)
    for page_num, page in enumerate(paged_books, start=1):
        columned_books = chunked(page, int(len(page) / 2))
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html'])
        )
        template = env.get_template('start_index.html')

        rendered_books = template.render(
            columns=columned_books,
            pages_num=pages_num,
            current_page=page_num
        )

        page_path = os.path.join('pages', f'rendered_index_{page_num}.html')
        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_books)

        if page_num == 1:
            with open('index.html', 'w', encoding="utf8") as file:
                file.write(rendered_books)


if __name__ == '__main__':
    server = Server()
    render_website()
    server.watch('start_index.html', render_website)
    server.serve(root='.', default_filename='pages/rendered_index_1.html')
