# PicoPawn — Pawn for WoW Ascension (3.3.5a)

PicoPawn is a port of the classic item-scoring addon **[Pawn](https://github.com/Road-block/Pawn)**
to the **WoW Ascension** client (WotLK 3.3.5a, build 12340).

Pawn shows a numerical **score** on item tooltips based on stat weights ("scales")
you choose, so you can tell at a glance which of two items is the upgrade. It also
adds upgrade arrows, a comparison window, and gem/enchant advice.

## Why a port?

The upstream [Road-block/Pawn](https://github.com/Road-block/Pawn) fork already targets
the 3.3.5 interface (`## Interface: 30300`) and uses only legacy APIs
(`GetItemInfo`, tooltip `Set*Item` hooks, `UnitClass`, `GetAddOnMetadata`), so it is
fundamentally compatible with the Ascension 12340 client. This port:

- **Rebrands** the addon to **PicoPawn** with its own saved variables, so it coexists
  cleanly with a stock Pawn install and keeps its own settings.
- Renames the addon folder/TOC and fixes the internal texture paths and
  `GetAddOnMetadata` lookups to match.
- Adds `/picopawn` and `/ppawn` slash commands (`/pawn` still works as an alias).

## Install

1. Download / clone this repository.
2. Copy the **`PicoPawn`** folder (the one containing `PicoPawn.toc`) into your
   Ascension `Interface\AddOns\` directory. The final path must be:
   `...\World of Warcraft\Interface\AddOns\PicoPawn\PicoPawn.toc`
3. Restart the client (or `/reload`) and make sure **PicoPawn** is enabled in the
   character-select AddOns list.
4. Open it in-game with `/picopawn`.

## Usage

- `/picopawn` — show or hide the PicoPawn window
- `/picopawn debug [ on | off ]` — spam parsing details to chat (for troubleshooting)
- `/picopawn backup` — export all your scales as text tags

Create a scale, assign stat weights (e.g. Strength = 1.0, Crit rating = 0.5), and
tooltips will start showing scores.

## Upgrade arrows & community scales

When a scale is **enabled**, item tooltips show that scale's **score**, plus a green
**`↑ +X% upgrade`** line whenever the item beats what you have equipped in that slot
(compared against the weaker item for rings/trinkets/one-hand weapons). The upgrade
line appears on the item's tooltip during comparison too — i.e. on the item you're
considering, next to your equipped item's tooltip. You get one line per enabled
scale, so a class shows one upgrade line per role at once (e.g. *Beast Mastery /
Marksmanship / Survival* for a Hunter). Only upgrades are shown (on by default via
the `ShowUpgrades` option); downgrades are omitted to keep tooltips clean.

Upgrades are also flagged with a **big green arrow** badge on the item's icon: both
at the top-left of its tooltip, and directly on the item's icon **in your bags (and
bank)**, so you can spot upgrades without even hovering. The badge appears only when
the item is an upgrade for one of your enabled scales; it updates automatically when
you change gear or toggle which scales are enabled.

In the PicoPawn window, the scale list's group headers (e.g. *Wowhead scales*,
*Ascension community scales*) are **collapsible** — click a header to fold/expand
that group; the state is remembered.

PicoPawn ships two sources of scales:

- **Built-in per-class/spec scales** (from Pawn's Wowhead data). On class-based
  realms (e.g. Bronzebeard) the scales for your class auto-enable, so arrows appear
  with no setup.
- **`Ascension` community scales** — stat weights submitted by players for specific
  realms, classes, and roles, bundled from the [`scales/`](scales/) folder. Scales
  matching your class auto-enable on first login; on classless realms
  (e.g. Voljin, Rexxar) nothing is force-enabled — pick the ones you want in the
  PicoPawn window.

### Contribute a scale

Tuned a good set of weights? Share it so it becomes an upgrade arrow for everyone:
export it in-game (Scales tab → export, or `/picopawn backup`) and open the
[**scale submission form**](https://github.com/matpicolli/wow-ascension--picopawn/issues/new?template=scale-submission.yml)
— it asks for the class, role, server, and version. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the full flow (and how maintainers turn
submissions into a bundled release via `tools/generate_ascension_scales.py`).

## Ascension notes

Ascension realms differ in how classes work, which affects Pawn's *default* scales
(the built-in Wowhead per-class/spec scales):

- **Class-based realms (e.g. Bronzebeard)** — behave like normal WotLK. The Wowhead
  scales auto-enable based on your class exactly as upstream intended.
- **Classless / expanded-class realms (e.g. Voljin, Rexxar with the new classes)** —
  `UnitClass` may not map to a stock class, so no scale auto-enables. This does **not**
  cause errors; you simply pick or build the scale that fits your chosen ability set.
  You can enable any of the built-in scales manually, or make a custom scale, from the
  PicoPawn window.

Ascension also has custom itemization and some custom stats. Standard WotLK stats
parse normally; any stat text Pawn doesn't recognize is listed under
`/picopawn debug on`, which is the starting point for adding Ascension-specific stat
support in a later pass.

**Item scaling:** on realms where items scale to your level, the client rebuilds a
hovered item's tooltip (adding its own *"Scaled item stats…"* note) after PicoPawn
has annotated it, which would wipe PicoPawn's score/upgrade lines. PicoPawn detects
this and re-applies its lines to the main tooltip, so scores and upgrade arrows
survive on scaled items. The client's own *"stats do not compare correctly"* note is
separate from PicoPawn.

## Credits

- **Pawn** by **Vger** — the original addon.
- **[Road-block/Pawn](https://github.com/Road-block/Pawn)** — the 3.3.5 fork this port is based on.

PicoPawn only repackages and adapts that work for Ascension; all scoring logic is theirs.
See `PicoPawn/Readme.htm` and `PicoPawn/Version history.htm` for the original documentation.
