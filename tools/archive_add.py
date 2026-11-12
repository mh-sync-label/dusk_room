"""Add tonight's poem (poem.json) to the archive list (archive.json). Run it each time poem.json is replaced:

    python3 tools/archive_add.py

The archive is a list only: date, title, author, collection, year, and, where the poem has one, the link to where it
lives (`source` and `url` in poem.json, for example an American Life in Poetry column), and, where the book is known,
its publisher and the publisher's page for it (`publisher` and `book_url`). No poem text is copied.
A poem with the same date replaces the earlier entry for that date; a poem.json without a date is refused.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
KEEP = ('date', 'title', 'author', 'collection', 'year', 'source', 'url', 'publisher', 'book_url')


def https_ok(u):
    """A plain https link: an https:// URL with a host and no user:password@ part."""
    s = str(u)
    try:
        parts = urlsplit(s)
    except ValueError:
        return False
    return s.startswith('https://') and bool(parts.hostname) and parts.username is None and parts.password is None and not any(c.isspace() for c in s)


def main():
    poem = json.loads((ROOT / 'poem.json').read_text(encoding='utf-8'))
    date = poem.get('date')
    if not (isinstance(date, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', date)):
        sys.exit('poem.json has no "date" (YYYY-MM-DD): add it, then run this again')
    url = poem.get('url')
    if url and not str(url).startswith('https://'):
        sys.exit('poem.json "url" must start with https://')
    book_url = poem.get('book_url')
    if book_url and not https_ok(book_url):
        sys.exit('poem.json "book_url" must be an https:// link to the publisher\'s page for the book')
    path = ROOT / 'archive.json'
    arc = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'poems': []}
    entry = {k: poem[k] for k in KEEP if poem.get(k) not in (None, '')}
    arc['poems'] = sorted([p for p in arc.get('poems', []) if p.get('date') != date] + [entry], key=lambda p: p['date'], reverse=True)
    path.write_text(json.dumps(arc, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('archive.json: %d poems; added %s, %s' % (len(arc['poems']), entry['date'], entry['title']))


if __name__ == '__main__':
    main()
