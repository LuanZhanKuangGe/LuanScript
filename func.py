import re
import requests
from tqdm import tqdm

# Iwara API 认证令牌
auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI1MmYyMjYyLWVjNjctNGU4Yi04OWI2LTdkOThjMDM4NmNhOSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJyb2xlIjoidXNlciIsInByZW1pdW0iOmZhbHNlLCJpc3MiOiJpd2FyYSIsImlhdCI6MTcyNjk5MzkxNywiZXhwIjoxNzI2OTk3NTE3fQ.BSWUHle8ToLx0wMDtxWzPCyktg7ikqXZIbbSaA57628'

# 设置请求头
iwara_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
    'Referer': 'https://www.iwara.tv/',
    'Origin': 'https://www.iwara.tv',
    'authorization': f'Bearer {auth_token}',
}

scrapy_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
}

def validateTitle(title):
    """
    验证并清理标题,移除不合法的文件名字符
    """
    return re.sub(r'[\\/:*?"<>|.]', '-', title)


def download_video(url, ref, filename):
    """
    下载视频并显示进度条
    
    参数:
    url: 视频下载链接
    ref: 引用页面
    filename: 保存的文件名
    
    返回:
    1: 下载成功
    0: 下载失败
    """
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': ref,
        'Origin': ref
    }

    # 发送GET请求,开启流式传输
    response = requests.get(url, stream=True, headers=headers)

    # 获取文件总大小
    total_size = int(response.headers.get('Content-Length', 0))

    # 设置下载块大小和进度条
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    custom_string = f"{filename.name}"
    progress_bar.set_description(custom_string)

    # 写入文件并更新进度条
    with open(filename, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)

    progress_bar.close()
    
    # 检查是否下载完整
    if total_size != 0 and progress_bar.n != total_size:
        return 0
    return 1