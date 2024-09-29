from pathlib import Path

folder_dict = {}
y_drive_path = Path('Y:\\')
z_drive_path = Path('Z:\\')
av_folder_path = Path(r'C:\Users\zhoub\Downloads\AV\整理完成')

def traverse_drive(drive_path, folder_dict):
    for path in drive_path.iterdir():
        if path.is_dir() and ' - ' in path.name:
            # 删除空文件夹
            if not any(path.iterdir()):
                path.rmdir()
                print(f"空文件夹已删除: {path}")
            else:
                if folder_dict.get(path.name) is None:
                    folder_dict[path.name] = {}
                # 查找.nfo文件并提取ID
                nfo_files = list(path.glob('*.nfo'))
                for nfo_file in nfo_files:
                    nfo_file_name = nfo_file.name
                    start_index = nfo_file_name.find(']')
                    end_index = nfo_file_name.find('-')
                    if start_index != -1 and end_index != -1:
                        id = nfo_file_name[start_index + 1:end_index]
                        if id == 'AVOP' or id == 'AVGP':
                            continue
                        if folder_dict[path.name].get(id) is None:
                            folder_dict[path.name][id] = 1
                        else:
                            folder_dict[path.name][id] += 1 

    return folder_dict

def traverse_av_folder(av_folder_path, folder_dict):
    for path in av_folder_path.rglob('*'):
        if path.is_file():
            file_name = path.name
            end_index = file_name.find('-')
            if end_index != -1:
                # 提取文件名中的ID
                id = file_name[:end_index]
                # 查找匹配的文件夹并移动文件
                for folder_name, id_dict in folder_dict.items():
                    if id in id_dict:
                        target_folder_path = av_folder_path / folder_name
                        target_folder_path.mkdir(parents=True, exist_ok=True)
                        new_file_path = target_folder_path / file_name
                        path.rename(new_file_path)
                        print(f"文件已移动: {path} -> {new_file_path}")
                        break

            else:
                print(f"文件名中未找到ID: {path}")

def rename_folder(folder_dict):
    # 找出folder dict中每个folder的item值的最高的5个key，并输出
    for folder_name, id_dict in folder_dict.items():
        # 按item值从高到低排序
        sorted_ids = sorted(id_dict.items(), key=lambda x: x[1], reverse=True)
        # 取前5个key，可能不足5个
        top_ids = sorted_ids[:5]
        # 按id再排序
        top_ids.sort(key=lambda x: x[0])
        
        new_folder_name = folder_name.split(' - ')[0].strip() + " - "
        for id, count in top_ids:
            new_folder_name += id + "_"
        new_folder_name = new_folder_name[:-1]
        if new_folder_name != folder_name:
            print(f"{folder_name} -> {new_folder_name}")
            old_folder_path = y_drive_path / folder_name
            new_folder_path = y_drive_path / new_folder_name
            if old_folder_path.exists():
                user_input = input(f"是否确认将 {old_folder_path} 重命名为 {new_folder_path}？输入'y'确认：")
                if user_input.lower() == 'y':
                    old_folder_path.rename(new_folder_path)
                    print(f"已将 {folder_name} 重命名为 {new_folder_name}")
                else:
                    print(f"取消重命名 {folder_name}")
            old_folder_path = z_drive_path / folder_name
            new_folder_path = z_drive_path / new_folder_name
            if old_folder_path.exists():
                user_input = input(f"是否确认将 {old_folder_path} 重命名为 {new_folder_path}？输入'y'确认：")
                if user_input.lower() == 'y':
                    old_folder_path.rename(new_folder_path)
                    print(f"已将 {folder_name} 重命名为 {new_folder_name}")
                else:
                    print(f"取消重命名 {folder_name}")

# 执行函数
traverse_drive(y_drive_path, folder_dict)
# traverse_drive(z_drive_path, folder_dict)
# rename_folder(folder_dict)
traverse_av_folder(av_folder_path, folder_dict)
