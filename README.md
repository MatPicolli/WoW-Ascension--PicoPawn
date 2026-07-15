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

## Credits

- **Pawn** by **Vger** — the original addon.
- **[Road-block/Pawn](https://github.com/Road-block/Pawn)** — the 3.3.5 fork this port is based on.

PicoPawn only repackages and adapts that work for Ascension; all scoring logic is theirs.
See `PicoPawn/Readme.htm` and `PicoPawn/Version history.htm` for the original documentation.
