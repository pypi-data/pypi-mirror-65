from ebooklib import epub
import mimetypes
import uuid
import re
import mimetypes
from urllib.parse import urlparse

from .book import Metadata, Chapter, Sentence, Image

from nltk.tokenize import sent_tokenize
from inscriptis import get_text, Inscriptis

class InscriptisImg(Inscriptis):
    def start_img(self, attrs):
        image_text = attrs.get('src', '')
        if image_text and not (self.cfg_deduplicate_captions and
                               image_text == self.last_caption):
            self.current_line[-1].content += '\n@[@{}\n'.format(image_text)
            self.last_caption = image_text

from lxml.html import fromstring
import json

def convert_epub(book):
    import nltk
    nltk.download('punkt')
    import base64
    cover = None
    coverType = ''
    cover_image = book.get_item_with_id('cover-image')
    if cover_image is not None:
        coverType = mimetypes.guess_type(cover_image.file_name)[0]
        cover = base64.b64encode(cover_image.get_content()).decode('utf-8')
    else:
        cover_id = book.get_metadata('OPF', 'cover')
        if len(cover_id) != 0:
            cover_id = cover_id[0][1]['content']
            cover_image = book.get_item_with_id(cover_id)
            if cover_image is not None:
                coverType = mimetypes.guess_type(cover_image.file_name)[0]
                cover = base64.b64encode(cover_image.get_content()).decode('utf-8')
            else:
                cover = ''
    title = book.get_metadata('DC', 'title')[0][0]
    author = book.get_metadata('DC', 'creator')[0][0]
    meta = Metadata(0, title, cover, author, coverType)
    return meta, _book_to_chapters(book)

def _get_item_by_href(book, href:str):
    for item in book.get_items():
        if item.get_name() in href or href in item.get_name():
            return item
    return None

def _get_contents(book):
    out = map(lambda item: {'content': _get_text(item.get_content()), 'name': item.file_name, 'id': item.id},
              filter(lambda item: isinstance(item, epub.EpubHtml), book.items)
              )
    return list(out)

def _get_text(html):
    tree = fromstring(html)
    return InscriptisImg(tree, display_images=True).get_text()

def _flatten(items):
    out = list()
    for item in items:
        if isinstance(item, tuple) or isinstance(item, list):
            section, subsection = item[0], item[1]
            href = ''
            if isinstance(section, epub.EpubHtml):
                href = section.get_id()
            elif isinstance(section, epub.Section) and section.href != '':
                href = section.href
            elif isinstance(section, epub.Link):
                href = section.href
            out.append({'title': section.title, 'href': href})
            out.extend(_flatten(subsection))
        elif isinstance(item, epub.Link):
            out.append({'title': item.title, 'href': item.href})
        elif isinstance(item, epub.EpubHtml):
            out.append({'title': item.title, 'href': item.file_name})
    for item in out:
        u = urlparse(item['href'])
        item['href'] = u.netloc + u.path
    return out

def _book_to_chapters(book):
    chaps = _flatten(book.toc)
    contents_ = _get_contents(book)

    for chap in chaps:
        for content in contents_:
            if chap['href'] == content['name']:
                content['chapter'] = chap['title']
    contents = []
    for chap in book.spine:
        href = chap[0]
        for content in contents_:
            if href == content['id']:
                contents.append(content)
    out = list()
    for content in contents:
        content['items'] = _content_to_items(book, content['content'])
        if 'chapter' not in content:
            content['chapter'] = None
        out.append(Chapter(str(uuid.uuid1()), content['chapter'], content['name'], content['items']))
    return out

def _content_to_items(book, content):
    raw = content.split('\n')
    raw = filter(lambda item: len(re.sub(r'[\s+]', '', item)) != 0, raw)
    raw = map(lambda item: item.strip(' \t\n\r'), raw)
    raw = list(raw)
    out = list()
    for sen in raw:
        if len(sen) >= 4 and sen[0:3] == '@[@':
            sen = sen[3:]
            import base64
            item = _get_item_by_href(book, sen)
            print(sen)
            imageType = mimetypes.guess_type(item.file_name)[0]
            image = base64.b64encode(item.get_content()).decode('utf-8')
            out.append(Image(str(uuid.uuid1()), image, imageType))
        else:
            sens = sent_tokenize(sen)
            for i in range(0, len(sens)):
                if i == 0:
                    out.append(Sentence(str(uuid.uuid1()), True, sens[i]))
                else:
                    out.append(Sentence(str(uuid.uuid1()), False, sens[i]))
    return out