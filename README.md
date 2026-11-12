# Dusk Room

A live three.js scene for maxxhillery.com: a light-oak desk in a quiet greyscale room at dusk, with tonight's
moon-matched poem on loose sheets in an open folder. Click the folder (or focus the scene and press Enter) to read;
long poems hang over the desk and scroll. A "Text only" view sits above the scene for anyone who would rather read,
and takes over on its own if the 3D scene cannot run.

- `index.html`: the page (three.js r147 from jsDelivr, pinned with integrity hashes). The viewer builds the Nook only;
  the other rooms (Rain, Linen, Café, Vathograph, Dressing room) stay in the code for the review build and are never
  built here. The scene code tracks the master page, `Desk_and_Folder_v<N>.html` in `Documents/PP/N_Room` on Maxx's
  Mac (currently v75): to bring a new master in, three-way merge it against the version the live page last took, keep
  the viewer's own lines (the Text-only view, the `DuskRoom` state, the assets in `assets/`, the closer reading
  distance `READ_D`/`READ_HALF`), and extract any new embedded data to `assets/`.
- `assets/`: the desk model (`desk.glb`), the brick wall's five maps, the Notturno paper (`notturno-paper.jpg`), the
  loading logo, the bookmark, the dust frames (`dust.json`), the café figures (`cafe-figures.json`, fetched only when
  the café is built), and the Vathograph picture and its cut-out chair (`vath-bg.jpg`, `vath-fg.png`, used only there).
  Kept as files rather than inlined so the page itself is small and the browser caches each asset on its own.
- `poem.json`: tonight's poem, `{ title, author, year, lines: [...], collection?, date?, source?, url?, phase?, note? }`. Replace it
  nightly; the page fetches it with no caching. One copy of the current poem is also baked into `index.html` (the
  `POEM` constant near the top of the text-view script) so the page is never empty while it loads.
- `text.html`: the poem alone, as a plain page, for a direct link.
- `archive.html` and `archive.json`: the poems that have run, as a list only (date, title, author, collection, year);
  no poem text is kept. After replacing `poem.json`, run `python3 tools/archive_add.py` to add it to the list.
  Each title links out to where the poem can be read (its `url`) or to a WorldCat library search; the poem that is
  up tonight (the same date as `poem.json`) is marked "up now" and links to the main page, and nothing dated after it is
  listed. The round chip at its head is `assets/notturno-logo.png`, the widget's mark, on a dark disc drawn in CSS.
- Where a poem lives elsewhere (an American Life in Poetry column, say), give `poem.json` two more fields:
  `"source": "American Life in Poetry"` and `"url": "https://..."`. The Text only view and `text.html`
  then show a "Read it at American Life in Poetry" link, and the archive links the poem's title there. Only `https://` links are shown.
- Printing: the Text only view and `text.html` have a "Print" link that prints the poem alone.
- Embedding: the page detects when it is inside an iframe and fills the frame edge to edge; `?embed=1` forces the same.
  `?still=1` turns off the slow camera drift. `?debug=1` logs every state change to the console and shows the frame
  time (ms per frame and fps, averaged over the last second), the shadow-map rate, and the pixel ratio in the stage's
  corner; the same numbers are at `DuskRoom.perf`.
- Lighting: two lights carry the Nook, the warm lamp on the folder and cool moonlight through the window, and the rest of
  the room falls toward a dark blue-grey. The moonlight follows tonight's phase: the moon in the window, the beam on the
  floor, and its strength all scale with the lit fraction. To review another night, `?illum=0..1` sets the lit fraction
  (0 new, 1 full, on tonight's side of full) and `?phase=0..1` sets the phase (0 new, 0.25 first quarter, 0.5 full, 0.75
  last quarter). The knobs are in the `ML` object near the top of `buildRoom()`.
- Reading: clicking the folder holds the room's last frame as a still, pushes it slightly toward the folder, and dissolves
  it into the page, so the move is smooth however slowly the room draws (`?move=fly` flies the camera there instead).
  The poem is drawn as its own high-resolution ink texture on a near-white sheet; on narrow (phone) frames it is set
  larger, and long lines turn over with a hanging indent. Each poem's sheet carries a few quiet marks (a fold, a turned
  corner, a pencil tick) seeded from the poem itself, so every reader sees the same sheet; `?sheet=<word>` previews
  another. The knobs are `MOVE`, `INK`, `SHEET`, `TALL`, and `WHITE` in `index.html`.
- Rendering cost: the shadow maps are redrawn every other frame while the room is still and every third while the camera
  is moving (they are drawn from the lights, so the camera's moves do not change them); the renderer asks for the
  high-performance GPU on two-GPU machines.

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
