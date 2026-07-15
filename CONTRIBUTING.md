# Contributing to PicoPawn

## Submitting a scale (for players — no coding needed)

A **scale** is a set of stat weights PicoPawn uses to score items. When a scale
is enabled, item tooltips show a green/red **upgrade arrow** and a percentage for
it — one line per scale, so a class can show one arrow per role (e.g. Beast
Mastery / Marksmanship / Survival for a Hunter).

Share your scale so it can be bundled for everyone:

1. **Build/tune your scale in-game.** Open PicoPawn with `/picopawn`, create a
   scale, and set your stat weights.
2. **Copy the scale tag.** In the **Scales** tab there's an export button; or run
   `/picopawn backup` to print every scale as a text tag. It looks like:
   ```
   ( Pawn: v1: "Beast Mastery": Agility=100, CritRating=64, HitRating=61, ... GemQualityLevel=4 )
   ```
3. **Open the submission form:**
   [**Submit a Pawn scale**](https://github.com/matpicolli/wow-ascension--picopawn/issues/new?template=scale-submission.yml).
   Fill in **class**, **role**, **server/realm**, **version**, and paste the tag.
4. Submit. A maintainer reviews it and adds it to the next addon update, where it
   becomes an upgrade arrow for everyone on that realm.

### Just want to use a single scale now?

You don't have to wait for a release. Any scale tag (from the form, the
[`scales/`](scales/) folder, or a friend) can be imported directly in-game:
open PicoPawn → **Scales** tab → **Import**, and paste the tag.

## Adding an accepted scale (for maintainers)

See [`scales/README.md`](scales/README.md). In short: add a `scales/*.json` file,
run `python tools/generate_ascension_scales.py`, and commit the regenerated
`PicoPawn/AscensionScales.lua`.

## Editing the addon code

The addon lives in [`PicoPawn/`](PicoPawn/). Note two Ascension-specific rules:

- **Line endings must stay CRLF.** The 3.3.5a client fails to parse an addon whose
  `.toc` uses Unix (LF) line endings, and the addon silently won't appear. The
  `.gitattributes` marks the addon's text files as binary so git preserves CRLF —
  don't "fix" that.
- **Keep the UTF-8 BOM** on the existing `.lua` files (the client and upstream
  Pawn use it).
