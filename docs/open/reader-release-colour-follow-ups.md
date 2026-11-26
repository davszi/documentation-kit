# Theme colours: two follow-ups for the reader release

Open work. The [`[theme_colors]` table](../../rules/site/authoring.md#theme-colours)
recolours the whole theme except two parts that belong to the reader, which
the reader release restructures. Both wait for that release, so its branch
can do them on its own files.

## The fold controls follow the table

`theme/components/fold-controls.js` writes its colours into the page as
literals, so they stay the kit's under any `[theme_colors]`:

- the bar of fold controls: its see-through navy background
  `rgba(14, 17, 23, 0.88)`, its button text `#cdd6e0` and its hover and
  pressed backgrounds `rgba(60, 70, 90, .5)` and `rgba(90, 105, 135, .45)`;
- the fold border `#666` and the four fold-type hues `#a99df0`, `#5dcaa5`,
  `#85b7eb` and `#f0997b`, also written in `chapter-reader.css`.

Done when the bar reads theme properties with the kit's value as fallback,
as `carousel.js` and `plot-toggles.js` do (`--control-rgb`, `--chip-text`,
`--chip-hover-rgb`), the default pages stay pixel-identical, and the fold
hues either follow the table or are named as kept in the authoring guide.

## The reader stylesheet's colour commit, redone

The commit "Express the chapter reader's colours through custom properties"
(`dc24c25` on branch `site-palette`) changes only colour values in
`theme/components/chapter-reader.css`. The reader release moves or removes
many of that file's rules, so the reader branch redoes the change on its
restructured file: every navy or grey literal reads a `:root` property of
`base.css`, see-through ones read the `--<name>-rgb` channels, and the group
tones read `--group-tone-N`.

Done when resolving every `:root` property in the reader branch's file before
and after gives the same text, and `tests/test_theme_colors.py` passes on the
reader branch.
