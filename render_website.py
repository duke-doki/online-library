import json
import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def render_website():
    with open('downloaded_books.json', 'r') as file:
        books_json = file.read()
    books = json.loads(books_json)
    columned_books = chunked(books, int(len(books)/2))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('index.html')

    rendered_books = template.render(columns=columned_books)

    with open('rendered_index.html', 'w', encoding="utf8") as file:
        file.write(rendered_books)


if __name__ == '__main__':
    server = Server()
    render_website()
    server.watch('index.html', render_website)
    server.serve(root='.', default_filename='rendered_index.html')
