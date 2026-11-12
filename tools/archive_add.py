"""Add tonight's poem (poem.json) to the archive list (archive.json). Run it each time poem.json is replaced:

    python3 tools/archive_add.py

The archive is a list only: date, title, author, collection, year, and, where the poem has one, the link to where it
lives (`source` and `url` in poem.json, for example an American Life in Poetry column). No poem text is copied.
A poem with the same date replaces the earlier entry for that date; a poem.json without a date is refused.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP = ('date', 'title', 'author', 'collection', 'year', 'source', 'url')


def main():
    poem = json.loads((ROOT / 'poem.json').read_text(encoding='utf-8'))
    date = poem.get('date')
    if not (isinstance(date, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', date)):
        sys.exit('poem.json has no "date" (YYYY-MM-DD): add it, then run this again')
    url = poem.get('url')
    if url and not str(url).startswith('https://'):
        sys.exit('poem.json "url" must start with https://')
    path = ROOT / 'archive.json'
    arc = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'poems': []}
    entry = {k: poem[k] for k in KEEP if poem.get(k) not in (None, '')}
    arc['poems'] = sorted([p for p in arc.get('poems', []) if p.get('date') != date] + [entry], key=lambda p: p['date'], reverse=True)
    path.write_text(json.dumps(arc, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('archive.json: %d poems; added %s, %s' % (len(arc['poems']), entry['date'], entry['title']))


if __name__ == '__main__':
    main()
