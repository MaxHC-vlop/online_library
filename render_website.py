import json
import os

from more_itertools import chunked
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape

def on_reload():
    with open("books_content.json", "r") as my_file:
        content_json = my_file.read()

    content = json.loads(content_json)

    content_2 = list(chunked(content, 2))

    content_3 = list(chunked(content_2, 10))

    folder = 'pages'

    os.makedirs(folder, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    for number, page in enumerate(content_3):

        filename = f'index{number}.html'

        page_path = os.path.join(folder, filename)

        rendered_page = template.render(
            content = page
        )

        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

if __name__ == '__main__':
    main()