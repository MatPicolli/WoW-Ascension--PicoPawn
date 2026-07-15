# Community scales

This folder holds the accepted community stat-weight scales. Each scale is one
`*.json` file. The generator in `../tools/generate_ascension_scales.py` turns
every file here into `../PicoPawn/AscensionScales.lua`, a scale provider that the
addon loads — so accepted scales show up in-game as upgrade arrows/percentages,
grouped by realm/class/role.

Players **submit** scales through the
[scale submission form](https://github.com/matpicolli/wow-ascension--picopawn/issues/new?template=scale-submission.yml)
(no git needed). Maintainers turn accepted submissions into a file here.

## File format

```json
{
  "name":    "Beast Mastery",
  "class":   "Hunter",
  "role":    "DPS (Ranged)",
  "server":  "Bronzebeard",
  "version": "3.3.5a",
  "author":  "SomePlayer",
  "notes":   "optional",
  "tag":     "( Pawn: v1: \"Beast Mastery\": Agility=100, CritRating=64, ... GemQualityLevel=4 )"
}
```

| Field     | Required | Meaning |
|-----------|----------|---------|
| `name`    | yes | Short display name for the scale. |
| `class`   | yes | Class name. On classless realms, use the closest archetype. |
| `role`    | yes | Tank / Healer / DPS (Melee) / DPS (Ranged) / DPS (Caster) / Other. |
| `server`  | yes | Realm the weights are tuned for (free text). |
| `version` | yes | Client/addon version it was tuned on. |
| `tag`     | yes | The Pawn export string. The generator reads the stat weights from it. |
| `author`  | no  | Credit. |
| `notes`   | no  | Anything else. |

Naming convention for files: `<server>-<class>-<role>.json` (lowercase,
hyphenated), e.g. `bronzebeard-hunter-bm.json`. Files starting with `example-`
are starter placeholders and can be replaced by real community data.

## Maintainer workflow (accepting a submission)

1. Review the submission issue. Sanity-check the tag (starts with `( Pawn: v1:`).
2. Add a `*.json` file here with the fields above.
3. Regenerate the addon provider:
   ```
   python tools/generate_ascension_scales.py
   ```
4. Commit both the new `scales/*.json` and the regenerated
   `PicoPawn/AscensionScales.lua`.

The generator:
- parses the stat weights out of the `tag` (ignoring `GemQualityLevel`, which is
  a scale property, not a stat),
- colours each scale by class,
- auto-enables scales whose class matches the player's class the first time a
  character logs in (so class-realm players get arrows with no setup; classless
  players enable what they want from the PicoPawn window).
