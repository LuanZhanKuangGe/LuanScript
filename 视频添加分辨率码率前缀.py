import os
import ctypes
import wmi


def get_file_attributes(file_path):
    # 获取文件属性
    attrs = ctypes.windll.kernel32.GetFileAttributesW(file_path)
    return attrs


def get_video_duration(file_path):
    # 使用wmi库获取视频时长
    wmp = wmi.WMI()
    media_info = wmp.Win32_MediaFile.where(f"Path='{file_path}'")

    if media_info:
        return int(media_info[0].Duration)
    else:
        return None


def get_videos_info_in_directory(directory):
    video_info_list = []

    # 列出目录中的所有文件
    files = os.listdir(directory)

    # 筛选视频文件
    video_files = [f for f in files if f.lower().endswith(('.mp4', '.avi', '.mkv', '.mov'))]

    for video_file in video_files:
        video_file_path = os.path.join(directory, video_file)

        # 获取文件属性
        attrs = get_file_attributes(video_file_path)

        # 获取视频时长
        duration = get_video_duration(video_file_path)

        if attrs and duration is not None:
            video_info_list.append({
                'file': video_file,
                'size': attrs,
                'duration': duration
            })

    return video_info_list


# 目录路径
directory_path = r'C:\Users\zhoub\Downloads'

# 获取目录下所有视频文件的信息
videos_info = get_videos_info_in_directory(directory_path)

# 打印视频信息
for video_info in videos_info:
    print(f"文件: {video_info['file']}")
    print(f"大小: {video_info['size']} bytes")
    print(f"时长: {video_info['duration']} seconds")
    print("=" * 30)
