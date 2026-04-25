from pathlib import Path
import re
import shutil

# === À ADAPTER ===
SOURCE_DIR = Path("../images")   # ex: export WP
TARGET_DIR = Path("../images/diapos")
IMAGE_EXTS = {".jpg", ".jpeg", ".webp", ".webp"}
# suffixes WP / retina / scaled
WP_SUFFIX_RE = re.compile(
    r"(?i)(?:-\d+x\d+(?:@2x)?|-scaled)$"
)

# doublons fréquents de WP / exports : -1, -2, 1, 2 en fin
TRAILING_DUP_RE = re.compile(r"(?i)(?:-\d+|\d+)$")


def normalize_stem(stem: str) -> str:
    s = stem.strip()

    # enlève les suffixes WP répétés en fin
    while True:
        new_s = WP_SUFFIX_RE.sub("", s)
        if new_s == s:
            break
        s = new_s

    # enlève un suffixe de doublon final simple
    s = TRAILING_DUP_RE.sub("", s).strip("-_ .")

    return s.casefold()


def is_variant_name(stem: str) -> bool:
    return bool(WP_SUFFIX_RE.search(stem)) or bool(TRAILING_DUP_RE.search(stem))


def score_file(path: Path) -> tuple:
    """
    Plus le score est grand, mieux c'est.
    Priorité :
    1. pas une variante WP / doublon numéroté
    2. fichier plus lourd
    """
    variant_penalty = 0 if is_variant_name(path.stem) else 1
    size_bytes = path.stat().st_size
    return (variant_penalty, size_bytes)


def main():
    if not SOURCE_DIR.exists():
        raise SystemExit(f"Source introuvable : {SOURCE_DIR}")

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(
        [
            p for p in SOURCE_DIR.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS
        ],
        key=lambda p: p.name.lower()
    )

    groups = {}
    for f in files:
        key = normalize_stem(f.stem)
        groups.setdefault(key, []).append(f)

    selected = []
    for _, candidates in groups.items():
        best = sorted(candidates, key=score_file, reverse=True)[0]
        selected.append(best)

    selected = sorted(selected, key=lambda p: p.name.lower())

    # vide le dossier cible
    for old in TARGET_DIR.iterdir():
        if old.is_file():
            old.unlink()

    copied_urls = []
    print("\nFICHIERS GARDÉS :\n")
    for src in selected:
        dst = TARGET_DIR / src.name
        shutil.copy2(src, dst)
        copied_urls.append(f"/diapos/{src.name}")
        print(src.name)

    print("\nLISTE ASTRO :\n")
    print("images={[")
    for url in copied_urls:
        print(f'  "{url}",')
    print("]}")


if __name__ == "__main__":
    main()