# Notturno

Notturno is a small widget for the Mac desktop. A poem releases every other day at sundown; its title appears below the
planet, and it can be read through the next day, until sunrise of the third day. The app's source is not in this repo:
this repo is its public home (the download, the update how-to, the archive of poems that have run, and a plain-text page
for tonight's poem), served by GitHub Pages at https://mh-sync-label.github.io/dusk_room/.

## Download and updating

- Download: https://github.com/mh-sync-label/dusk_room/releases/latest/download/Notturno.dmg (always the latest release;
  the releases are at https://github.com/mh-sync-label/dusk_room/releases/latest).
- Updating: the app's "update available" notice is driven by the Notturno endpoint (its `poem.json` carries the latest
  version number), not by anything in this repo. The notice leads to `update.html`, which walks through downloading the
  new `Notturno.dmg`, quitting the running Notturno, dragging the new one onto Applications, choosing Replace, and opening
  it again (including the Privacy & Security "Open Anyway" step, which happens once for each new version).

### Addresses the shipped app opens

The shipped app opens exactly these three addresses:

- https://mh-sync-label.github.io/dusk_room/update.html
- https://mh-sync-label.github.io/dusk_room/archive.html
- https://github.com/mh-sync-label/dusk_room/releases/latest/download/Notturno.dmg

They must never move or be renamed, and the repo must not be renamed (its name is part of all three).

### What is not in this repo

The app's source, the Notturno endpoint's source, and the master of `update.html` live off-repo, in the owner's Notturno
folder (the master is `Update_Page/update.html`). Do not edit `update.html` here: when it changes, it is published over
this file from that master.

## What lives here

- `index.html`: the front page for the app (download, and links to the pages below). When it is opened inside a frame,
  or with any of the room's query parameters, it forwards to `room/` instead (see docs/room.md).
- `update.html`: how to replace the app with a newer version. Opened by the shipped app; never move or rename it, and do
  not edit it here (it is published from its off-repo master, above).
- `archive.html` + `archive.json`: the list of poems that have run (no poem text). `archive.html` is opened by the shipped
  app; never move or rename it. Keep `archive.json`'s name too (the page loads it).
- `text.html`: tonight's poem alone, as a plain page, for a direct link. Keep the name.
- `assets/`: what the app's pages use: `notturno-logo.png` (the chip at the head of `archive.html` and the front page),
  and `notturno-wordmark.svg` (the wordmark, built by `tools/make_wordmark.py`; nothing in the repo loads it).
- `room/`: the 3D Dusk Room scene (`room/index.html`) and its own assets (`room/assets/`). Documented in `docs/room.md`.
- `moon.html`, `moon-next.html`, `moon/`: website embeds, left where they are because the website may load them by
  these addresses. `moon.html` draws tonight's Notturno moon for the site's /notturno logo (it links to
  https://www.maxxhillery.com/). `moon-next.html` is currently an identical copy of `moon.html`; keep both. `moon/` holds
  eight phase images (`moon1.png` to `moon8.png`); nothing in this repo references them.
- `tools/archive_add.py`: adds a poem's archive entry to `archive.json` (below).
- `tools/make_wordmark.py`: builds the wordmark from a scan: `python3 tools/make_wordmark.py <scan> assets/notturno-wordmark.svg`
  (with no second argument it writes `notturno-wordmark.svg` in the current folder).
- `docs/room.md`: the room's documentation.
- `.nojekyll`: tells GitHub Pages to serve the files as they are.

## Tonight's poem, and where poems live

The poems live only on the Notturno endpoint (`https://notturno-poems.notturno-poema.workers.dev`), and nothing in this
repo holds poem text (the repo is public). Never commit a poem file.

The endpoint's `poem.json` is tonight's poem:
`{ title, author, year, lines: [...], collection?, publisher?, book_url?, date?, source?, url?, phase?, note? }`.
`text.html` (and the room's Text only view) read it with no caching; if the endpoint cannot be reached, or does not answer
with a poem, a quiet note says the poem couldn't be loaded just now, in place of the poem.

- Where a poem lives elsewhere (an American Life in Poetry column, say), give the poem (on the endpoint, and in the poem
  file kept off GitHub) two more fields: `"source": "American Life in Poetry"` and `"url": "https://..."`. The room's Text
  only view and `text.html` then show a "Read it at American Life in Poetry" link, and the archive links the poem's title
  there. Only `https://` links are shown.
- When the book a poem comes from is known, give the poem its publisher and the publisher's own page for the book, as
  part of the nightly step (before running `tools/archive_add.py`, which carries them into the archive):
  `"collection": "The Rain in the Trees", "publisher": "Knopf", "book_url": "https://www.penguinrandomhouse.com/books/113558/the-rain-in-the-trees-by-w-s-merwin/"`.
  The archive then reads "from *The Rain in the Trees* · 1988 · Knopf", with the book's name linked to that page. The tool
  refuses a `book_url` that is not a plain `https://` link, and the page ignores one. Leave both out when the book is not
  known; the entry then shows just the title and the poet (and the book's name, if known, unlinked).

## The archive

`archive.html` and `archive.json` are the poems that have run, as a list only (date, title, author, collection, year, and
the book's publisher and link where known); no poem text is kept. The page says each poem was up for two nights.

Each time a poem runs, add its entry to `archive.json`, by hand or with the tool:

    python3 tools/archive_add.py ~/Documents/PP/Notturno/Poems/poem_2026-11-18.json

The argument is the path to a poem file kept off GitHub. The tool copies only the list fields (`date`, `title`, `author`,
`collection`, `year`, `source`, `url`, `publisher`, `book_url`) and never the text, and writes `archive.json` at the top of
the repo (wherever you run it from). It refuses a poem file without a `date` (`YYYY-MM-DD`), a `url` that does not start
with `https://`, and a `book_url` that is not a plain `https://` link; a poem with the same date replaces the earlier entry
for that date. With no path it reads `poem.json` at the top of the repo, which should not exist there any more. Never
commit the poem file itself.

How the page shows the list:

- Where the book is known, its name links to the publisher's page for it (`book_url`); a title links out only where the
  poem has its own page (`url`), and otherwise is plain text.
- The poem that is up tonight (the same date as the endpoint's `poem.json`) is marked "up now" (its title is not a link),
  and nothing dated after it is listed.
- Since 2026-11-18 the page reads the Notturno endpoint first (`https://notturno-poems.notturno-poema.workers.dev`): its
  `archive.json` is merged with this one (field by field: the endpoint's value wins, and this file fills what it lacks),
  and "tonight" is the date in the endpoint's `poem.json`. If the endpoint can't be reached, the page lists this site's
  `archive.json` alone, with no night marked "up now".
- The round chip at its head is `assets/notturno-logo.png`, the widget's mark, on a dark disc drawn in CSS; it links to
  https://www.maxxhillery.com/notturno.

## Releasing a new version

Upload the new build to a GitHub Release on this repo, with the asset named exactly `Notturno.dmg`, and mark it as the
latest release. The shipped app, `update.html`, and the front page link to `releases/latest/download/Notturno.dmg`, which only resolves
when the latest release has an asset of exactly that name.

## The room

The 3D Dusk Room scene (a light-oak desk at dusk with tonight's poem in an open folder, embedded on maxxhillery.com) is
now a secondary part of the repo, at `room/`. Its documentation (the page notes, lighting, reading, rendering cost,
embedding parameters, and its state object) is in [docs/room.md](docs/room.md).
