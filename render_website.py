import json
import os

from environs import Env
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

env = Env()
env.read_env()
books = env.str('BOOKS')


def render_website():
    global books
    with open(f'{books}.json', 'r') as file:
        books = json.load(file)

    books_for_page = 20
    paged_books = list(chunked(books, books_for_page))
    pages_num = len(paged_books)
    os.makedirs('pages', exist_ok=True)
    for page_num, page in enumerate(paged_books, start=1):
        columns = 2
        columned_books = chunked(page, int(len(page) / columns))
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
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(parent_dir)
    server = Server()
    render_website()
    server.watch('online-library/start_index.html', render_website)
    server.serve(root=parent_dir, default_filename='online-library/index.html')
