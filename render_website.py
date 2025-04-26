import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked


def on_reload(books):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    two_collumns_books = list(chunked(books, 2))

    rendered_page = template.render(
        books=two_collumns_books,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

def main():
    with open("meta_data.json", "r", encoding="utf-8") as my_file:
        books_json = my_file.read()
    books = json.loads(books_json)
    on_reload(books)

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()