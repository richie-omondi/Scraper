import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.route("/")
def hello_world():

    
    news_sites = [
  {
     'https://cryptonews.com':{"props": ["h4", "a"], "data":"a"}
  },            
  {
     'https://beincrypto.com':{"multi-news-card": ["a"], "data": "img"}
  },
  {
     'https://news.bitcoin.com':{"story": ["a"], "data": "img"}
  },
  {
     'https://cointelegraph.com':{"main-news-controls__item": ["div", "a"], "data": "a"}   
  },
  {
     'https://cointelegraph.com':{"main-press-releases__item": ["a"], "data": "img"}
  },
  {
     'https://cointelegraph.com':{"post-card__header": ["a"], "data": "span"}
  }
 ]
    almost = []
    for news_site in news_sites:
    
        keys = list(news_site.keys())
        base_url = keys[0]
        response = requests.get(base_url).text
        soup = bs(response, features="html.parser")
        web_link = news_site[base_url]
        specific_item_obj = list(web_link.keys())
        specific_item = specific_item_obj[0]
        specific_item_text = web_link["data"]
        many_news = soup.find_all(class_= specific_item)
        for news in many_news:
            order = web_link[specific_item]
            content = news
            length_of_order = len(order)-1
            for index, structure in enumerate(order): 
                content = content.find(structure) 
                if content:
                    if length_of_order == index:
                        if base_url in content['href']:
                            gotten_link = content['href']
                        else:
                            gotten_link = base_url+content['href']
                        text = ""
                        where_to_find_text = content.find(specific_item_text)
                        if content.name == specific_item_text:
                            text = content.get_text()
                        elif where_to_find_text and where_to_find_text.name == "img":
                            text = where_to_find_text["alt"] 
                        elif where_to_find_text and where_to_find_text.name == "span":
                            text = where_to_find_text.get_text()         
                        almost.append({gotten_link:text})

    return render_template("home.html", almost=almost)

@app.template_filter()
def listerize(what):
    return list(what)

@app.template_filter()
def first(lst):
    return lst[0]

@app.template_filter()
def get_text(article, link):
    return article[link]

    if __name__ == "__main__":
        app.run(debug=True)