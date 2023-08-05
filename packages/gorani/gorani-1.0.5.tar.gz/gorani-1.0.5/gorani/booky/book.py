from collections import Set

from ebooklib import epub

import typing
import xml.etree.ElementTree as xml
import xml.sax.saxutils as saxutils

from gorani.utils import split_sentence


def read_epub(path):
    from .epub_converter import convert_epub
    book = epub.read_epub(path)
    return Book(*convert_epub(book))

class Item:
    def __init__(self, kind: str):
        self.kind = kind

    @staticmethod
    def from_xml(tag):
        if tag.tag == 'sentence':
            return Sentence.from_xml(tag)
        else:
            return Image.from_xml(tag)

    @classmethod
    def from_dict(cls, obj):
        if 'kind' not in obj:
            return Sentence.from_dict(obj)
        if obj['kind'] == 'sentence':
            return Sentence.from_dict(obj)
        elif obj['kind'] == 'image':
            return Image.from_dict(obj)
        else:
            raise Exception('FUCK')

class Image(Item):
    def __init__(self, id, image, imageType):
        super().__init__('image')
        self.id = id
        self.image = image
        self.imageType = imageType

    def to_xml(self):
        out = xml.Element('image', imageType=str(self.imageType).lower(), id=self.id)
        out.text = saxutils.escape(self.image)
        return out

    @staticmethod
    def from_xml(tag):
        id = tag.get('id')
        return Image(id, tag.text,  tag.get('imageType'))

    def to_dict(self):
        return {
            'id': self.id,
            'image': self.image,
            'imageType': self.imageType,
            'kind': self.kind
        }

    @classmethod
    def from_dict(cls, obj):
        return cls(obj['id'], obj['image'], obj['imageType'])


class Sentence(Item):
    def __init__(self, id, start, content):
        super().__init__('sentence')
        self.id = id
        self.start = start
        self.content = content

    def to_xml(self):
        out = xml.Element('sentence', start=str(self.start).lower(), id=self.id)
        out.text = saxutils.escape(self.content)
        return out

    @staticmethod
    def from_xml(tag):
        start = False
        start_raw = tag.get('start')
        if start_raw == 'true':
            start = True
        id = tag.get('id')
        return Sentence(id, start, tag.text)

    def to_dict(self):
        return {
            'id': self.id,
            'start': self.start,
            'content': self.content,
            'kind': self.kind
        }

    @classmethod
    def from_dict(cls, obj):
        return cls(obj['id'], obj['start'], obj['content'])

class Chapter(typing.NamedTuple):
    id: str
    title: str
    fileName: str
    items: typing.List[Item]

    def to_xml(self):
        title = self.title
        if title is None:
            title = ''
        out = xml.Element('chapter', id=self.id, title=title, fileName=self.fileName)
        for item in self.items:
            out.append(item.to_xml())
        return out

    @classmethod
    def from_xml(cls, tag):
        items = list()
        for item in tag:
            items.append(Item.from_xml(item))
        title = tag.get('title')
        id = tag.get('id')
        filename = tag.get('fileName')
        return cls(id, title, filename, items)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'fileName': self.fileName,
            'items': [item.to_dict() for item in self.items]
        }

    @classmethod
    def from_dict(cls, obj):
        items = [Item.from_dict(item) for item in obj['items']]
        return cls(obj['id'], obj['title'], obj['fileName'], items)

class Metadata(typing.NamedTuple):
    id: str
    title: str
    cover: str
    author: str
    coverType: str

    def to_xml(self):
        out = xml.Element('meta')
        xml.SubElement(out, 'id').text = self.id
        xml.SubElement(out, 'title').text = self.title
        xml.SubElement(out, 'author').text = self.author
        xml.SubElement(out, 'coverType').text = self.coverType
        if self.cover is not None:
            xml.SubElement(out, 'cover').text = self.cover
        return out

    @classmethod
    def from_xml(cls, tag):
        id = tag.find('id').text
        title = tag.find('title').text
        author = tag.find('author').text
        coverType = tag.find('coverType').text
        cover_raw = tag.find('cover')
        cover = None
        if cover_raw is not None:
            cover = cover_raw.text
        return cls(id, title, cover, author, coverType)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'cover': self.cover,
            'author': self.author,
            'coverType': self.coverType
        }

    @classmethod
    def from_dict(cls, obj: dict):
        return cls(obj['id'], obj['title'], obj['cover'], obj['author'], obj['coverType'])


class Book:
    meta: Metadata
    chapters: typing.List[Chapter]

    def __init__(self, meta, chapters):
        self.meta = meta
        self.chapters = chapters
        self._init_cache()

    def _init_cache(self):
        self.id_to_sentence_context = dict()
        self.id_to_sentence = dict()
        self.id_to_item = dict()
        self.id_to_chapter = dict()
        for chap in self.chapters:
            self.id_to_chapter[chap.id] = chap
            def get_surrounding_text(sentence_id):
                for i in range(0, len(chap.items)):
                    if not isinstance(chap.items[i], Sentence):
                        continue
                    if chap.items[i].id == sentence_id:
                        return ' '.join(
                            s.content for s in chap.items[max(0, i - 3):min(len(chap.items), i + 3)] if isinstance(s, Sentence))
                raise Exception("wtf")

            for item in chap.items:
                self.id_to_item[item.id] = item
                if isinstance(item, Sentence):
                    self.id_to_sentence[item.id] = item.content
                    self.id_to_sentence_context[item.id] = get_surrounding_text(item.id)

    def compare_by_wordset(self, wordset):
        b = self.get_wordset()
        onlyb = len(b.difference(wordset)) / len(b)
        # onlya = len(a.difference(b)) / len(a)
        return onlyb

    def compare_with_book(self, book):
        a = self.get_wordset()
        b = book.get_wordset()
        onlyb = len(b.difference(a)) / len(b)
        # onlya = len(a.difference(b)) / len(a)
        return onlyb

    def get_wordset(self):
        out = set()
        for chap in self.chapters:
            for sen in chap.items:
                for word in split_sentence(sen.content):
                    out.add(word.lower())
        return out

    def get_item(self, id):
        return self.id_to_item.get(id, None)

    def get_sentence(self, sid):
        return self.id_to_sentence.get(sid, None)


    def to_dict(self):
        return {
            'meta': self.meta.to_dict(),
            'chapters': [chap.to_dict() for chap in self.chapters]
        }

    def to_xml(self):
        out = xml.Element('book')
        out.append(self.meta.to_xml())
        chapstag = xml.Element('chapters')
        for chap in self.chapters:
            chapstag.append(chap.to_xml())
        out.append(chapstag)
        return xml.tostring(out, encoding='utf8', method='xml')

    @classmethod
    def from_dict(cls, data):
        meta = Metadata.from_dict(data['meta'])
        chaps = [Chapter.from_dict(chap) for chap in data['chapters']]
        return cls(meta, chaps)

    @classmethod
    def read_xml(cls, path):
        with open(path, 'r') as f:
            root = xml.fromstring(f.read())

            metatag = root.find('meta')
            meta = Metadata.from_xml(metatag)
            chapstag = root.find('chapters')
            chapters = list()
            for chap in chapstag:
                chapters.append(Chapter.from_xml(chap))

            return cls(meta, chapters)
