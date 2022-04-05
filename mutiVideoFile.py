from pathlib import Path

p = Path("W:\\")

for d in p.iterdir():
    if d.is_dir():
        c = 0
        for f in d.iterdir():
            if f.suffix != ".nfo" and f.suffix!=".jpg" and f.suffix!=".png":
                c += 1
        if c > 1:
            print(d)
        c = 0