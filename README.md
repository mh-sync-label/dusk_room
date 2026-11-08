# Dusk Room

A live three.js scene for maxxhillery.com: a light-oak desk in a quiet greyscale room at dusk, with tonight's
moon-matched poem on loose sheets in an open folder. Click the folder (or focus the scene and press Enter) to read;
long poems hang over the desk and scroll. A "Text only" view sits above the scene for anyone who would rather read,
and takes over on its own if the 3D scene cannot run.

- `index.html`: the page (three.js r147 from jsDelivr, pinned with integrity hashes). The viewer builds the Nook only;
  the other rooms (Rain, Linen, Café, Vathograph) stay in the code for the review build and are never built here.
- `assets/`: the desk model (`desk.glb`), the brick wall's five maps, the loading logo, the bookmark, the dust frames
  (`dust.json`), and the café figures (`cafe-figures.json`, fetched only when the café is built). Kept as files rather
  than inlined so the page itself is small and the browser caches each asset on its own.
- `poem.json`: tonight's poem, `{ title, author, year, lines: [...], collection?, date?, phase?, note? }`. Replace it
  nightly; the page fetches it with no caching. One copy of the current poem is also baked into `index.html` (the
  `POEM` constant near the top of the text-view script) so the page is never empty while it loads.
- `text.html`: the poem alone, as a plain page, for a direct link.
- Embedding: the page detects when it is inside an iframe and fills the frame edge to edge; `?embed=1` forces the same.
  `?still=1` turns off the slow camera drift. `?debug=1` logs every state change to the console.

## State

The page keeps its state in one object, `window.DuskRoom`, defined in the first script of `index.html` (before three.js
loads). Four facts and a few flags; everything the reader sees follows from them.

| fact | values | meaning |
|---|---|---|
| `scene` | `loading` · `ready` · `failed` | the 3D room's own life |
| `panel` | `scene` · `text` | what the reader is looking at; `text` is forced once the scene fails |
| `view` | `room` · `reading` · review views | where the camera is; `reading` is on the sheet |
| `poem` | `baked` · `tonight` | whether `poem.json` has arrived |
| flags | `moving`, `orbit`, `visible`, `longPoem`, `reason` | camera in transition; review orbit; stage on screen; sheet hangs over the desk; why the scene failed |

Read it with `DuskRoom.snapshot()`, or from the DOM: `<body data-scene data-panel data-view data-poem data-moving>`.
Change it only through the transitions: `showText()`, `showScene()`, `toggleText()`, `read()`, `leave()`, `goTo(view)`,
`setPoem(poem)`, `sceneReady()`, `sceneFailed(reason)`. Listen with `DuskRoom.on(fn)` or the `dusk:state` event on
`document` (`detail.state`, `detail.changed`). `render()` inside the store is the only code that writes the state to the
DOM (body classes, labels, aria), and `DuskRoom.copy` holds every line of interface text. The older `window.__toText`,
`__showText`, `__goTo`, `__setPoem`, `__nudge`, and `__setPalette` hooks still work.

Built from the project source (Blender `bpy` scene + viewer source); see that project's README and SPEC.
