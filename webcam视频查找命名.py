import os

def get_folder_names(directory):
    try:
        folder_names = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
        return folder_names
    except Exception as e:
        print(f"获取文件夹名时出错: {e}")
        return []

def check_files_in_folders(directory, folder_names):
    for folder_name in folder_names:
        folder_path = os.path.join(directory, folder_name)
        try:
            files = os.listdir(folder_path)
            for file in files:
                file_name = os.path.splitext(file)[0]
                if '-' in file_name:
                    prefix = file_name.split('-')[0].strip()
                    prefix = prefix.replace('#', '')
                    if prefix != folder_name:
                        print(f"文件夹名: {folder_name}，文件名: {file}")
        except Exception as e:
            print(f"检查文件时出错: {e}")

# 获取V:\【裸舞】下的文件夹名
directory = r"V:\【裸舞】"
folder_names = get_folder_names(directory)
print(f"找到以下文件夹: {folder_names}")

# 检查文件夹下的文件
check_files_in_folders(directory, folder_names)

