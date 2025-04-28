import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked
from os.path import split


def on_reload():
    with open("meta_data.json", "r", encoding="utf-8") as my_file:
        books_json = my_file.read()
    books = json.loads(books_json)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    ten_lists_books = list(chunked(books, 10))
    for number, list_books in enumerate(ten_lists_books):
        two_collumns_books = list(chunked(list_books, 2))
        count_pages = len(ten_lists_books)
        for list_book in list_books:
            genres = list_book["genres"].replace(".", "").split(",")
            rendered_page = template.render(
                books=two_collumns_books,
                count_pages=count_pages,
                this_page=number,
                genres=genres,
            ) 
            file_path = os.path.join('pages', f'index{number}.html')
            with open(file_path, 'w', encoding="utf8") as file:
                file.write(rendered_page)
        

def main():

    if not os.path.isdir("pages"):
        os.makedirs("pages")

    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()