import json
import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape


if __name__ == '__main__':
    with open('downloaded_books.json', 'r') as file:
        books_json = file.read()
    books = json.loads(books_json)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('index.html')

    rendered_books = template.render(books=books)

    with open('rendered_index.html', 'w', encoding="utf8") as file:
        file.write(rendered_books)
