from pathlib import Path

MangaPath = Path("P:\\Manga\\")

for manga in MangaPath.iterdir():
    if manga.stem.find("[中国翻訳]") == -1:
        name = manga.stem.replace("[DL版]", "")
        name = name.replace("[無修正]", "")
        name = name.replace("[WebP]", "")
        name = name.split(" + ")[0]
        name = name.strip()
        print(name)
