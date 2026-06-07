"""Bulk find/replace + page rename for SE Hot Water & Pergolas scaffold."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SELF_NAME = Path(__file__).name

REPLACEMENTS = [
    ("https://geelongroofrestorations.com.au", "https://sehotwater.com.au"),
    ("geelongroofrestorations.com.au", "sehotwater.com.au"),
    ("geelongroofrestorations", "sehotwater"),
    ("Geelong Roof Restorations", "SE Hot Water &amp; Pergolas"),
    ("Geelong roof restoration", "Berwick decking &amp; pergola"),
    ("Geelong&rsquo;s specialist", "Berwick&rsquo;s specialist"),
    ("Geelong&rsquo;s", "Berwick&rsquo;s"),
    ("Greater Geelong", "South East Melbourne"),
    ("Surf Coast Shire", "Endeavour Hills Hills"),
    ("Bellarine", "Narre Warren"),
    ("Surf Coast", "Endeavour Hills Hills"),
    ("Geelong, the Bellarine and the Surf Coast", "Berwick, Narre Warren and the Endeavour Hills Hills"),
    ("Geelong, the Bellarine, and the Surf Coast", "Berwick, Narre Warren, and the Endeavour Hills Hills"),
    ("Bell Park", "Nar Nar Goon"),
    ("Corio", "Garfield"),
    ("Ocean Grove", "Emerald"),
    ("Torquay", "Gembrook"),
    ("Geelong", "Berwick"),
    ('"3220"', '"3806"'),
    ("VIC 3220", "VIC 3806"),
    ("3220", "3806"),
    ("-38.1499", "-38.0395"),
    ("144.3617", "145.3458"),
    ("Roof Restoration Services", "Decking, Pergola &amp; Outdoor Living Services"),
    ("roof restoration & replacement contractors", "decking, pergola &amp; outdoor living specialists"),
    ("Roof restoration", "Decking"),
    ("roof restoration", "decking project"),
    ("Roof Restoration", "Decking"),
    ("ROOF RESTORATION", "DECKING &amp; PERGOLAS"),
    ("specialist roof restoration", "specialist decking"),
    ("free roof inspections", "free design consultations"),
    ("Free roof inspections", "Free design consultations"),
    ("Free Inspection", "Free Consultation"),
    ("free inspection", "free consultation"),
    ("RoofingContractor", "GeneralContractor"),
    ("Roof Cleaning &amp; Pressure Washing", "Timber Decking"),
    ("Roof Painting &amp; Sealing", "Composite Decking"),
    ("Tile Restoration &amp; Repointing", "Pergolas &amp; Verandas"),
    ("Metal Roof Restoration", "Alfresco &amp; Outdoor Kitchens"),
    ("Gutter Replacement", "Deck Restoration"),
    ("Roof cleaning &amp; pressure washing", "Timber decking"),
    ("Roof painting &amp; sealing", "Composite decking"),
    ("Tile restoration &amp; repointing", "Pergolas &amp; verandas"),
    ("Metal roof restoration", "Alfresco &amp; outdoor kitchens"),
    ("Gutter replacement", "Deck restoration"),
    ("Roof Cleaning", "Timber"),
    ("Roof Painting", "Composite"),
    ("Tile Restoration", "Pergolas"),
    ("Metal Restoration", "Alfresco"),
    ("/services/roof-cleaning/", "/services/timber-decking/"),
    ("/services/roof-painting/", "/services/heat-pump-hot-water/"),
    ("/services/tile-restoration/", "/services/solar-hot-water/"),
    ("/services/metal-restoration/", "/services/alfresco-outdoor-kitchens/"),
    ("/services/gutter-replacement/", "/services/deck-restoration/"),
    ("/newtown/", "/narre-warren/"),
    ("/belmont/", "/cranbourne/"),
    ("/highton/", "/cockatoo/"),
    ("/armstrong-creek/", "/emerald/"),
    ("/lara/", "/hampton-park/"),
    ("/greater-geelong/", "/south-east-melbourne/"),
    ("Newtown", "Narre Warren"),
    ("Belmont", "Cranbourne"),
    ("Highton", "Cockatoo"),
    ("Armstrong Creek", "Emerald"),
    ("Lara", "Hampton Park"),
    ("quotes@geelongroofrestorations.com.au", "quotes@sehotwater.com.au"),
    (">G</text>", ">P</text>"),
]

EXTENSIONS = {".astro", ".md", ".toml", ".mjs", ".json", ".xml", ".txt", ".html", ".css", ".js"}

def patch_file(p):
    try:
        s = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    out = s
    for old, new in REPLACEMENTS:
        out = out.replace(old, new)
    if out != s:
        p.write_text(out, encoding="utf-8")
        return True
    return False

def main():
    PAGES = ROOT / "src" / "pages"
    for old, new in [
        ("newtown.astro", "officer.astro"),
        ("belmont.astro", "beaconsfield.astro"),
        ("highton.astro", "cockatoo.astro"),
        ("armstrong-creek.astro", "emerald.astro"),
        ("lara.astro", "berwick-upper.astro"),
        ("greater-geelong.astro", "south-east-melbourne.astro"),
    ]:
        o, n = PAGES / old, PAGES / new
        if o.exists() and not n.exists():
            o.rename(n); print(f"renamed: {old} -> {new}")

    SVC = PAGES / "services"
    for old, new in [
        ("roof-cleaning.astro", "timber-decking.astro"),
        ("roof-painting.astro", "composite-decking.astro"),
        ("tile-restoration.astro", "pergolas.astro"),
        ("metal-restoration.astro", "alfresco-outdoor-kitchens.astro"),
        ("gutter-replacement.astro", "deck-restoration.astro"),
    ]:
        o, n = SVC / old, SVC / new
        if o.exists() and not n.exists():
            o.rename(n); print(f"renamed: {old} -> {new}")

    changed = 0
    for p in ROOT.rglob("*"):
        if not p.is_file(): continue
        if p.suffix not in EXTENSIONS: continue
        if "node_modules" in p.parts or "dist" in p.parts: continue
        if p.name == SELF_NAME: continue
        if patch_file(p):
            changed += 1

    pkg = ROOT / "package.json"
    if pkg.exists():
        s = pkg.read_text(encoding="utf-8")
        s = s.replace('"name": "geelongroofrestorations"', '"name": "sehotwater"')
        pkg.write_text(s, encoding="utf-8")

    print(f"Done. {changed} files patched.")

if __name__ == "__main__":
    main()
