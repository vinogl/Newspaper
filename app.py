import os
from flask import Flask, render_template, request, redirect, send_from_directory
from feed_read import get_json, get_articles, get_feed

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


@app.route('/')
def main_page():
    page_info = get_json(path=json_path["Pages"])  # 获取页面的相应信息
    feed_list = get_json(path=json_path["feed_list"])  # 获取RSS的订阅源信息

    return render_template("Main.html", page_info=page_info, feed_list=feed_list, list_path=json_path["feed_list"])


@app.route('/<feed_key>', methods=['GET', 'POST'])
def home_page(feed_key):
    """
    主页，显示所有文章
    能根据前端传回的表单返回指定的订阅页面
    """
    if request.method == 'POST':
        """根据表单post信息选择feed_key"""
        feed_key = request.form.get('feed_key')  # 获取表单返回的feed_source
        return redirect('/%s' % feed_key)

    page_info = get_json(path=json_path["Pages"])  # 获取页面的相应信息
    feed_list = get_json(path=json_path["feed_list"])  # 获取RSS的订阅源信息

    feed_path = os.path.join(json_path["feeds"], feed_key + '.json')  # 已下载订阅的路径

    if not os.path.exists(feed_path):
        """若还未下载订阅源到本地，则执行下载操作"""
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
