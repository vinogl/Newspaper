import os
from feed_read import get_json, get_feed


def download_feeds(json_path):
    """
    下载rss_feed订阅源到本地
    """
    feed_list = get_json(path=json_path["feed_list"])  # 获取RSS的订阅源信息
    for key, value in feed_list.items():
        """将订阅内容下载到本地"""
        get_feed(url=value, path=os.path.join(json_path["feeds"], key + '.json'))


def remove_feeds(json_path):
    """
    删除本地的rss_feed订阅源
    """
    for root, dirs, files in os.walk(json_path["feeds"]):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print('已删除 \"%s\"' % file_path)


if __name__ == '__main__':
    from app import json_path as jpath

    operate = input('需要执行的操作(remove(r)/download(d): ')
    if operate not in ['r', 'd']:
        print('输出错误，请按照提示输入！')

    if operate == 'r':
        remove_feeds(json_path=jpath)
    elif operate == 'd':
        download_feeds(json_path=jpath)
    else:
        print('终止操作！')
