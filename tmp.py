import json
with open('tmp.json', 'r') as file:
    database = json.load(file)
    sorted_keys = sorted(database, key=database.get, reverse=True)
    sorted_dict = {k: database[k] for k in sorted_keys}
    print(sorted_dict)


with open("tmp.json", "w", encoding="utf8") as fp:
    json.dump(sorted_dict, fp, ensure_ascii=False)