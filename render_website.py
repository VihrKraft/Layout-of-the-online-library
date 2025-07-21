import os
import json
import argparse

from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


COLLUMNS_NUMBER = 2
BOOKS_ON_PAGE = 10


def on_reload():
    parser = argparse.ArgumentParser(description='Программа создает локальный сервер для отслеживания изменений на сайте')
    parser.add_argument('--json', '-j', help='Путь к json файлу', default='meta_data.json')
    args = parser.parse_args()
    with open(args.json, 'r', encoding='utf-8') as my_file:
        books = json.load(my_file)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    ten_lists_books = list(chunked(books, BOOKS_ON_PAGE))
    for number, list_books in enumerate(ten_lists_books):
        two_collumns_books = list(chunked(list_books, COLLUMNS_NUMBER))
        count_pages = len(ten_lists_books)
        for list_book in list_books:
            genres = list_book['genres'].replace('.', '').split(',')
            rendered_page = template.render(
                books=two_collumns_books,
                count_pages=count_pages,
                this_page=number,
                genres=genres,
            ) 
            file_path = os.path.join('pages', f'index{number}.html')
            with open(file_path, 'w', encoding='utf8') as file:
                file.write(rendered_page)
        

def main():

    os.makedirs('pages', exist_ok=True)

    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index0.html')


if __name__ == '__main__':
    main()