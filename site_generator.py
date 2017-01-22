import os
import json
from jinja2 import Environment,FileSystemLoader
import markdown

CONFIGFILE = 'config.json'
TEMPLATESDIR = 'templates'
HTMLDIR = 'html'
ARTICLESDIR = 'articles'

def open_config_json(config_file):
    with open(config_file) as config_json:
        config = json.load(config_json)
    return config

def load_markdown_artilce(markdown_file):
    with open(os.path.join(ARTICLESDIR,markdown_file)) as article:
        article_md = article.read()
    article_html = markdown.markdown(article_md,output_format='html5')
    return article_html

def prepare_article(title,content):
    env = Environment(loader=FileSystemLoader(TEMPLATESDIR))
    template = env.get_template('article.html')
    return template.render({
                 'title' : title ,
                 'content' : content })

def prepare_directory(path):
    if os.path.exists(path):
        return True
    else:
        try:
            os.mkdir(path)
            return True
        except:
            return False


def save_article(path,output_html):
    with open(path,'w') as output_file:
        output_file.write(output_html)



if __name__ == '__main__':
    articles_config = open_config_json(CONFIGFILE)
    #html_markdown = load_markdown_artilce('articles/0_tutorial/8_cli.md')
    for topic in [ slug['slug'] for slug in articles_config['topics']]:
        if prepare_directory(os.path.join(HTMLDIR,topic)):
            articles = [{
                'source' : article['source'],
                'title' : article['title'],
                 'topic': article['topic']}
                        for article in articles_config['articles']
                            if article['topic'] == topic]
            for article in articles:
                prepare_directory()
                prepered_html = prepare_article(article['title'],load_markdown_artilce(article['source']))
                save_article(os.path.join(HTMLDIR,topic,article['source']),prepered_html)
        else:
            pass
