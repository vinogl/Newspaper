from datetime import datetime, timedelta
import feedparser
import json


def time_diff(time):
    """
    计算某时刻到现在时刻的差，并返回指定内容
    """
    time_now = datetime.now()  # 获取当前时间
    diff = time_now - time
    if diff.days / 365 >= 1:
        print(diff.days / 365)
        return '%d年前' % int(diff.days / 365)
    elif diff.days / 12 >= 1:
        return '%d个月前' % int(diff.days / 12)
    elif diff.days >= 1:
        return '%d天前' % int(diff.days)
    elif diff.days >= 0:
        if diff.seconds / 3600 >= 1:
            return '%d小时前' % round(diff.seconds / 3600)
        elif diff.seconds / 60 >= 1:
            return '%d分钟前' % round(diff.seconds / 60)
        elif diff.seconds >= 0:
            return '%d秒前' % round(diff.seconds)
    else:
        return '未知时间'


def get_json(path):
    """
    读取json文件
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_feed(url, path):
    """
    从url获取订阅源的解析，并保存到本地path
    """
    print('将 \"%s\" 下载到 \"%s\"...' % (url, path))
    feed = feedparser.parse(url)
    with open(path, 'w') as f:
        f.write(json.dumps(feed, ensure_ascii=False))


def get_articles(path):
    """
    根据get_feed方法下载的订阅源内容，返回所提取内容
    """
    feed = get_json(path=path)

    feed_len = len(feed["entries"])  # 获取到的文章数量
    articles = []  # 用于储存所需内容

    for i, item in enumerate(feed["entries"]):
        """将所需内容保存到临时词典"""
        time = datetime(*item["published_parsed"][:5]) + timedelta(hours=8)  # 读取的时间为GMT时间，与北京时间相差8小时
        temp_dic = {
            'art_id': i+1,
            'total': feed_len,
            'title': item["title"],
            'author': item["author"] if "author" in item.keys() else None,
            'content': item["summary"],
            'time': time.strftime('%Y-%m-%d %H:%M'),
            'time_diff': time_diff(time),
            'link': item["link"]
        }
        articles.append(temp_dic)

    return feed["feed"]["link"],  articles  # 返回所需文章内容、官网url
