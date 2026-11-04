# Dusk Room

A live three.js scene for maxxhillery.com: a light-oak desk in a quiet greyscale room at dusk, with tonight's
moon-matched poem on loose sheets in an open folder. Click the folder to read; long poems hang over the desk and
scroll.

- `index.html`: the page (three.js r147 from jsDelivr; the desk model is embedded).
- `poem.json`: tonight's poem, `{ title, author, year, lines: [...], collection?, date?, phase?, note? }`. Replace it nightly.
- Embed on the website with `?embed=1` to show the scene alone.

Built from the project source (Blender `bpy` scene + viewer source); see that project's README and SPEC.
