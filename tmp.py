from pathlib import Path
import pymediainfo

def rename_videos_with_resolution_prefix(folder_path):
    for video_file in Path(folder_path).rglob('*'):
        if video_file.is_file() and video_file.suffix in ['.mp4', '.mkv', '.avi']:  # 根据需要添加视频格式
            media_info = pymediainfo.MediaInfo.parse(video_file)
            for track in media_info.tracks:
                if track.track_type == 'Video':
                    width = track.width
                    height = track.height

                    resolution_tag = f'[{(round(width/1024))}k] '
                    if '] [' in video_file.name:
                        continue
                    if '] ' in video_file.name:
                        tag = video_file.stem.split(' ')[0]
                        name = video_file.stem.split('] ')[1]
                        if 'k' not in tag:
                            new_file_name = f"{tag} {resolution_tag}{name}{video_file.suffix}"
                        else:
                            new_file_name = f"{resolution_tag}{name}{video_file.suffix}"

                    new_file_path = video_file.parent / new_file_name
                    video_file.rename(new_file_path)
                    print(f"重命名文件: {video_file} -> {new_file_path}")

rename_videos_with_resolution_prefix(r'D:\VREN')

