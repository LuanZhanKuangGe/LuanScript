from pathlib import Path

director_list = {}

for nfo_file_path in Path(r"N:\AV").rglob("*.nfo"):
    with open(nfo_file_path, 'r', encoding='utf8') as file:
        nfo_content = file.readlines()
        for line in nfo_content:
            if "director" in line.strip():
                director = line.strip().replace("<director>","").replace("</director>","")
                if director != "有码导演" and director != "无码导演":
                    if not director_list.get(director):
                        director_list[director] = 0
                    director_list[director] += 1

sorted_items = sorted(director_list.items(), key=lambda x: x[1], reverse=True)
for key, value in sorted_items:
    print(f"{key}: {value}")