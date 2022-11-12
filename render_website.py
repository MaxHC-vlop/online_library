import json
import os
import shutil

from more_itertools import chunked
from livereload import Server
from jinja2 import Environment, FileSystemLoader
from jinja2 import select_autoescape


def get_books_description():
    filename = 'books_content.json'

    with open(filename, 'r') as file:
        books_description = json.load(file)

    return books_description


def on_reload(folder='pages'):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    books_description = get_books_description()

    number_columns = 2
    number_books_column = 10

    chunked_books_description = list(
        chunked(books_description, number_columns)
    )
    pages_books_description = list(
        chunked(chunked_books_description, number_books_column)
    )
    number_pages = len(pages_books_description)

    for number_page, page in enumerate(pages_books_description, start=1):

        filename = f'index{number_page}.html'

        page_path = os.path.join(folder, filename)

        rendered_page = template.render(
            page_content = page,
            number_page = number_page,
            number_pages = number_pages
        )

        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    folder = 'pages'

    if os.path.exists(folder):
        shutil.rmtree(folder)

    os.makedirs(folder, exist_ok=True)

    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
