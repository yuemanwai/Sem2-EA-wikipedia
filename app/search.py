import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import MultifieldParser,QueryParser
from flask import render_template, request
from flask_babel import _
from app.models import Post
from . import app

index_dir = os.path.join(os.getcwd(), 'index_dir')
schema = Schema(id=ID(stored=True), title=TEXT(stored=True), content=TEXT(stored=True))

# 創建Whoosh索引
def create_index():
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    ix = create_in(index_dir, schema)
    writer = ix.writer()
    # 將數據庫中的內容加入索引
    posts = Post.query.all()
    for post in posts:
        writer.add_document(id=str(post.id), title=post.title, content=post.body)
    writer.commit()


# 執行全文搜索
def search(query):
    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        parser = MultifieldParser(['title', 'content'], schema=schema)
        parsed_query = parser.parse(query)
        # 直接用"A"來搜尋, 都係return none
        # parsed_query = QueryParser("title", ix.schema).parse("A")
        results = searcher.search(parsed_query)
        return results


@app.route('/search')
def search_route():
    keyword = request.args.get('q', '')
    results = search(keyword)
    return render_template('search_results.html.j2', title=_('Search results'),results=results, keyword=keyword)