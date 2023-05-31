import os

folder_path = r'N:\HentaiPicture\madoucun'  # 文件夹路径

# 获取文件夹中所有的文件
file_list = os.listdir(folder_path)

# 遍历文件列表
for filename in file_list:
    if filename.endswith('.zip') and filename.startswith('['):
        # 获取文件的绝对路径
        old_filepath = os.path.join(folder_path, filename)

        # 解析出原始文件名和后缀
        name_start = filename.index('[') + 1
        name_end = filename.index(']')
        name = filename[name_start:name_end]
        extension = filename[name_end + 1:]

        # 构造新的文件名
        new_filename = name + '[' + extension

        # 构造新的文件路径
        new_filepath = os.path.join(folder_path, new_filename)

        # 重命名文件
        os.rename(old_filepath, new_filepath)