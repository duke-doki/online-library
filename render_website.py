import json
import os
import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def render_website():
    with open('downloaded_books.json', 'r') as file:
        books_json = file.read()
    books = json.loads(books_json)
    paged_books = chunked(books, 20)

    os.makedirs('pages', exist_ok=True)
    for page_num, page in enumerate(paged_books):
        columned_books = chunked(page, int(len(page) / 2))
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html'])
        )
        template = env.get_template('index.html')

        rendered_books = template.render(columns=columned_books)

        page_path = os.path.join('pages', f'rendered_index_{page_num}.html')
        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_books)


if __name__ == '__main__':
    server = Server()
    render_website()
    server.watch('index.html', render_website)
    start_page_path = os.path.join('pages', 'rendered_index_0.html')
    server.serve(root='.', default_filename=start_page_path)
