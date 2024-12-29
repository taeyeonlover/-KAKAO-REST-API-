from flask import Flask, request, render_template
from flask_paginate import Pagination, get_page_args
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search_books():
    if request.args.get('query'):
        
        search_query = request.args.get('query')
        search_type = request.args.get('search_type') 

        page, per_page, offset= get_page_args(per_page=10)

        books,meta = get_book_results(search_query,search_type,page)

        if meta['total_count'] > 500:
            total = 500
        else:
            total = meta['total_count']

        pagination = Pagination(page=page, total=total, per_page=per_page)

        return render_template('result.html', books=books, search=search_query,
                                target=search_type, pagination=pagination)

    return render_template('home.html')

def get_book_results(query, target, page=1):
    api_key = 'f7e96caf0b74c0a73e82f724b9db79fe'
    url = f'https://dapi.kakao.com/v3/search/book?query={query}&target={target}&page={page}'
    headers = {'Authorization': f'KakaoAK {api_key}'}

    response = requests.get(url, headers=headers)
    data = response.json()['documents']
    meta = response.json()['meta']
    books = []

    for book_data in data:
        book = {
            'title': book_data['title'],
            'authors': book_data['authors'],
            'publisher': book_data['publisher'],
            'sale_price': book_data['sale_price'],
            'thumbnail': book_data['thumbnail'],
            'url': book_data['url'],
            'published_year': book_data['datetime'][:4]
        }
        books.append(book)

    return books, meta

def get_target(search_type):  
    if search_type == 'title':
        return 'title'
    elif search_type == 'author':
        return 'person'
    elif search_type == 'publisher':
        return 'publisher'
    else:
        return 'title' 

    


if __name__ == '__main__':
    app.run(debug=True)