import json

from livereload import Server, shell

from jinja2 import Environment, FileSystemLoader, select_autoescape

def on_reload():
    with open("books_content.json", "r") as my_file:
        content_json = my_file.read()

    content = json.loads(content_json)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        content = content
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

if __name__ == '__main__':
    main()