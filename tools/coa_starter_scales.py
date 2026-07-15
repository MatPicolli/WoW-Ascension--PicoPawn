#!/usr/bin/env python3
"""Generate BASIC starter scales for the Conquest of Azeroth (CoA) classes.

CoA is Ascension's expansion with 21 custom, classless-style heroes. There are no
published per-spec stat weights (and the detailed wiki pages block automated
access), so these are *role-template* scales: the primary stat is weighted highest
and role-appropriate secondaries follow. They are meant as sane starting points
that the community refines through the scale submission form.

Roles per class were taken from the Conquest of Azeroth wiki / class summaries
(July 2026). Damage type per role (spell power vs. strength vs. agility) is a
best-effort guess from each class's fantasy; correct anything that's off by
editing CLASSES below and re-running, or just submit a tuned scale in-game.

This writes one JSON file per (class, role) into scales/conquest-of-azeroth/.
After running it, run tools/generate_ascension_scales.py to rebuild the addon.
"""

import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "scales", "conquest-of-azeroth")
SERVER = "Conquest of Azeroth"
VERSION = "CoA (3.3.5a)"
AUTHOR = "PicoPawn (basic starter)"

# Role -> stat-weight template. Stat names are the ones PicoPawn understands
# (same as the built-in Wowhead scales). GemQualityLevel is a scale property.
TEMPLATES = {
    "Tank (Str)":     {"Stamina": 100, "DodgeRating": 85, "DefenseRating": 85, "ParryRating": 80, "Strength": 45, "Agility": 45, "Armor": 45, "BlockValue": 35, "ExpertiseRating": 35, "HitRating": 25, "Ap": 10},
    "Tank (Agi)":     {"Stamina": 100, "Agility": 90, "DodgeRating": 80, "Armor": 55, "DefenseRating": 30, "ExpertiseRating": 25, "HitRating": 20, "Strength": 15, "Ap": 10, "CritRating": 5},
    "Healer":         {"SpellPower": 100, "Spirit": 75, "HasteRating": 65, "Intellect": 60, "Mp5": 50, "CritRating": 45, "Stamina": 0.1},
    "Caster DPS":     {"SpellPower": 100, "HitRating": 80, "HasteRating": 70, "CritRating": 60, "Intellect": 35, "Spirit": 3, "Stamina": 0.1},
    "DPS (Melee-Str)": {"Strength": 100, "HitRating": 80, "ExpertiseRating": 75, "CritRating": 65, "HasteRating": 60, "ArmorPenetration": 55, "Ap": 45, "Agility": 35, "Stamina": 0.1},
    "DPS (Melee-Agi)": {"Agility": 100, "HitRating": 80, "ExpertiseRating": 75, "CritRating": 65, "HasteRating": 60, "ArmorPenetration": 55, "Ap": 45, "Strength": 25, "Stamina": 0.1},
    "DPS (Ranged)":   {"Agility": 100, "HitRating": 80, "CritRating": 65, "HasteRating": 58, "ArmorPenetration": 50, "Ap": 45, "Intellect": 3, "Stamina": 0.1},
}

# Human-facing role label (what shows in-game) per template key.
ROLE_LABEL = {
    "Tank (Str)": "Tank",
    "Tank (Agi)": "Tank",
    "Healer": "Healer",
    "Caster DPS": "DPS (Caster)",
    "DPS (Melee-Str)": "DPS (Melee)",
    "DPS (Melee-Agi)": "DPS (Melee)",
    "DPS (Ranged)": "DPS (Ranged)",
}

# class name -> list of role template keys it can fill.
CLASSES = {
    "Necromancer":      ["Caster DPS"],
    "Pyromancer":       ["Caster DPS", "Healer"],
    "Cultist":          ["Tank (Str)", "Caster DPS", "Healer"],
    "Starcaller":       ["Healer", "Tank (Str)", "DPS (Ranged)"],
    "Sun Cleric":       ["Tank (Str)", "Healer", "Caster DPS"],
    "Tinker":           ["DPS (Ranged)", "Healer"],
    "Runemaster":       ["Caster DPS"],
    "Primalist":        ["Tank (Str)", "Healer", "DPS (Melee-Str)"],
    "Reaper":           ["Tank (Str)", "DPS (Melee-Str)"],
    "Venomancer":       ["Tank (Agi)", "Healer", "DPS (Melee-Agi)", "Caster DPS"],
    "Chronomancer":     ["Caster DPS", "Healer"],
    "Bloodmage":        ["Tank (Str)", "Healer", "Caster DPS"],
    "Guardian":         ["Tank (Str)", "DPS (Melee-Str)"],
    "Stormbringer":     ["Caster DPS"],
    "Felsworn":         ["Tank (Str)", "DPS (Melee-Str)", "Caster DPS"],
    "Barbarian":        ["DPS (Melee-Str)", "Tank (Str)"],
    "Witch Doctor":     ["Caster DPS", "Healer"],
    "Witch Hunter":     ["Tank (Agi)", "DPS (Ranged)", "DPS (Melee-Agi)"],
    "Knight of Xoroth": ["Tank (Str)", "DPS (Melee-Str)"],
    "Templar":          ["Tank (Str)", "DPS (Melee-Str)"],
    "Ranger":           ["DPS (Ranged)", "DPS (Melee-Agi)"],
}


def fmt_num(v):
    return str(int(v)) if v == int(v) else repr(v)


def build_tag(name, weights):
    body = ", ".join("%s=%s" % (k, fmt_num(v)) for k, v in weights.items())
    return '( Pawn: v1: "%s": %s, GemQualityLevel=4 )' % (name, body)


def slugify(s):
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-").replace("--", "-")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    count = 0
    for klass, roles in CLASSES.items():
        # De-duplicate the visible role label per class (e.g. two melee variants).
        seen_labels = {}
        for tmpl_key in roles:
            label = ROLE_LABEL[tmpl_key]
            seen_labels[label] = seen_labels.get(label, 0) + 1
            suffix = "" if seen_labels[label] == 1 else " %d" % seen_labels[label]
            role_label = label + suffix
            scale_name = "%s %s" % (klass, role_label)
            weights = TEMPLATES[tmpl_key]
            data = {
                "name": scale_name,
                "class": klass,
                "role": role_label,
                "server": SERVER,
                "version": VERSION,
                "author": AUTHOR,
                "notes": "Basic role-template starter for Conquest of Azeroth; tune and resubmit for accurate weights.",
                "tag": build_tag(scale_name, weights),
            }
            fn = "%s-%s.json" % (slugify(klass), slugify(role_label))
            with open(os.path.join(OUT_DIR, fn), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            count += 1
    print("Wrote %d CoA starter scales to %s" % (count, os.path.relpath(OUT_DIR, REPO)))


if __name__ == "__main__":
    main()
