from ebooklib import epub
from typing import List, Union
from dataclasses import dataclass

@dataclass
class Chapter:
    title: str
    content: str

class Ebook:
    def __init__(self, title: str, lang: str = "en", author: str = ""):
        self._book = epub.EpubBook()

        self._book.set_title(title)
        self._book.set_language(lang)

        book_id = hex(hash(title + author))
        self._book.set_identifier(book_id)

        if author:
            self._book.add_author(author)

        self._book.spine = ['nav']
        self._book.toc = []

    def __create_epub_chapter(self, chapter: Chapter) -> epub.EpubHtml:
        chapter_filename = f"{chapter.title}.xhtml"
        epub_chapter = epub.EpubHtml(title=chapter.title, file_name=chapter_filename)
        epub_chapter.set_content(chapter.content)

        self._book.add_item(epub_chapter)
        return epub_chapter

    def add_chapter(self, chapter: Chapter):
        epub_chapter = self.__create_epub_chapter(chapter)

        self._book.spine.append(epub_chapter)
        self._book.toc.append(epub.Link(epub_chapter.file_name, chapter.title))

    def add_section(self, name: str, chapters: List[Chapter]):
        epub_chapters = [self.__create_epub_chapter(c) for c in chapters]

        self._book.toc.append((epub.Section(name), epub_chapters))
        self._book.spine.extend(epub_chapters)

    def write_ebook(self, path: str):
        self._book.add_item(epub.EpubNcx())
        self._book.add_item(epub.EpubNav())

        epub.write_epub(path, self._book)