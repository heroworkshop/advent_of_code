from collections import namedtuple
from pprint import pprint

from misc import dr_who_books

Book = namedtuple("book", "tv_num library_num title author audiobook")

def parse_book_line(line):
    parts = line.split()
    tv_num = int(parts.pop(0))
    library_num = int(parts.pop(0))
    title = []
    while True:
        p = parts.pop(0)
        if p[-2:] in ("th", "nd", "st") and p[0] in "0123456789":
            doctor = p
            break
        title.append(p)
    title = " ".join(title)
    author = []
    while True:
        p = parts.pop(0)
        if p[0] in "0123456789":
            break
        author.append(p)
    author = " ".join(author)
    audiobook = parts.pop()
    return Book(tv_num, library_num, title, author, audiobook)


class BookIterator:
    def __init__(self, line_iterator):
        self.line_iterator = line_iterator

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            line = next(self.line_iterator)
            try:
                book = parse_book_line(line)
                return book
            except (IndexError, ValueError):
                pass


def parse_books(lines):
    book_iterator = BookIterator(iter(lines))
    return list(book_iterator)

def main():
    lines = dr_who_books.RAW.split("\n")
    books = parse_books(lines)
    pprint(books)

if __name__ == "__main__":
    main()
