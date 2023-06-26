from pathlib import Path

import xml.etree.ElementTree as ET

list = []

# 创建一个 Path 对象来表示目标目录
directory_path = Path(r"N:\AV")

# 使用 rglob 方法筛选文件
files = directory_path.rglob("*.nfo")

# 遍历匹配的文件
for file in files:
    if file.is_file() and file.name.startswith('[SD]'):
        # 解析NFO文件
        tree = ET.parse(file)
        root = tree.getroot()

        # 提取所需的信息
        year = root.find("release").text

        # 打印信息
        print(file, year)

        list.append((file, year))

list = sorted(list, key=lambda x: x[1])

for item in list:
    print(item)