import os
from pathlib import Path
import shutil

# 设置漫画目录路径
manga_path = Path(r"D:\HentaiPicture\Manga")

# 遍历目录下的所有文件
for file in manga_path.iterdir():
    if file.is_file():
        # 获取文件名
        filename = file.name
        
        # 检查文件名是否包含[]
        if "]" in filename:
            # 提取[]中的作者名
            actor = filename.split("]")[0].replace("[","")
            
            # 检查是否存在对应作者文件夹
            actor_folder = manga_path / actor
            if actor_folder.exists() and actor_folder.is_dir():
                try:
                    # 移动文件到作者文件夹
                    shutil.move(str(file), str(actor_folder / filename))
                    print(f"已移动 {filename} 到 {actor} 文件夹")
                except Exception as e:
                    print(f"移动文件 {filename} 失败: {e}")
            # else:
            #     print(f"未找到作者文件夹: {actor}")
        else:
            print(f"文件名格式不正确: {filename}")
