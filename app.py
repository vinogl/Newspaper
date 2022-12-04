import os
import json
from flask import Flask, render_template, request, redirect, send_from_directory
from feed_read import get_json, get_articles, get_feed
from feeds_operation import download_feeds, remove_feeds

app = Flask(__name__)

json_path = {
    "Pages": "json/Pages.json",  # 页面填充信息
    "feed_list": "json/feed_list.json",  # RSS订阅url信息
    "feeds": "json/feeds/",  # 获取的feed内容
}


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', 'POST'])
def main_page():
    """
    主页面，显示所有的订阅源名字，
    并链接到其各订阅源的home页面
    """
    if request.method == 'POST':
        """根据返回的表单，执行对本地feed文件的相应操作"""
        operation = request.form.get("operation")  # 获取操作
        if operation == "download":
            download_feeds(json_path=json_path)  # 下载所有feed内容
        elif operation == "remove":
            remove_feeds(json_path=json_path)  # 删除所有feed内容

    page_info = get_json(path=json_path["Pages"])  # 获取页面的相应信息
    feed_list = get_json(path=json_path["feed_list"])  # 获取RSS订阅源信息

    return render_template("Main.html", page_info=page_info, feed_list=feed_list)


@app.route('/edit', methods=['GET', 'POST'])
def edit_feeds():
    """
    修改feed_list的内容
    """
    if request.method == 'POST':
        """将返回表单的RSS订阅源信息，填入feed_list"""
        list_content = list(filter(None, request.form.get("display").split('\r\n')))  # 将订阅源信息分组
        list_json = {}  # 用于储存填入内容

        for item in list_content:
            """逐条将填入内容写入到词典"""
            feed_key, feed_url = item.split(': ')
            list_json.update({feed_key: feed_url})  # 将RSS订阅源信息写入词典，之后方便存入json文件

        with open(json_path["feed_list"], 'w') as f:
            """将更新的RSS的订阅源信息填入feed_list"""
            f.write(json.dumps(list_json, ensure_ascii=False))

    page_info = get_json(path=json_path["Pages"])  # 获取页面的相应信息
    feed_list = get_json(path=json_path["feed_list"])  # 获取RSS订阅源信息

    display = ''  # 用于储存在编辑框中展示的内容
    for feed_key, feed_url in feed_list.items():
        """将RSS订阅源信息逐行写入展示字符串"""
        display += '%s: %s\n' % (feed_key, feed_url)

    return render_template("Edit.html", page_info=page_info, display=display)


@app.route('/<feed_key>', methods=['GET', 'POST'])
def home_page(feed_key):
    """
    单个订阅源的home页面，显示所有文章
    能根据前端传回的表单返回指定的订阅页面
    """
    refresh = None  # 默认不更新feed内容
    if request.method == 'POST':
        """根据表单post信息选择feed_key"""
        _feed_key = request.form.get('feed_key')  # 获取表单返回的feed_key
        refresh = request.form.get('refresh')  # 是否更新feed内容
        if _feed_key is not None:  # 判断提交的表单是否为feed_key
            return redirect('/%s' % _feed_key)

    page_info = get_json(path=json_path["Pages"])  # 获取页面的相应信息
    feed_list = get_json(path=json_path["feed_list"])  # 获取RSS订阅源信息

    feed_path = os.path.join(json_path["feeds"], feed_key + '.json')  # 已下载订阅的路径

    if not os.path.exists(feed_path) or refresh is not None:
        """若还未下载订阅源到本地，或者提交了更新表单，则执行下载操作"""
        get_feed(url=feed_list[feed_key], path=feed_path)

    original_link, articles = get_articles(path=feed_path)  # 获取官网url、所有文章的所需内容

    return render_template('Home.html', page_info=page_info, feed_key=feed_key, original_link=original_link,
                           feed_list=feed_list, articles=articles)


@app.route('/<feed_key>/<int:art_id>', methods=['GET', 'POST'])
def article_page(feed_key, art_id):
    """
    每篇文章的全文阅读页面
    art_id为文章的id（文章的顺序作为文章的id）
    """
    if request.method == 'POST':
        """提交表单更换文章后，重定向到指定文章"""
        art_id = int(request.form.get('art_id'))  # 获取art_id
        return redirect('/%s/%d' % (feed_key, art_id))

    page_info = get_json(path=json_path["Pages"])  # 获取页面的相应信息

    feed_path = os.path.join(json_path["feeds"], feed_key + '.json')  # 已下载订阅的路径

    original_link, articles = get_articles(path=feed_path)  # 获取官网url、所有文章的所需内容
    article = articles[art_id - 1]  # 获取当前文章的内容

    return render_template('Article.html', page_info=page_info, feed_key=feed_key, original_link=original_link,
                           articles=articles, article=article)


if __name__ == '__main__':
    app.run()
