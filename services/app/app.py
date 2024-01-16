import datetime
import os
import requests

from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configurer le mode debug en fonction de la variable d'environnement
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG') == '1'


@app.route('/test')
def test():
    return f'Test {datetime.datetime.now()}'


@app.route('/')
def home():
    # response = requests.get('http://52.200.82.146', headers={'User-Agent': 'Mozilla/5.0', 'Host': 'www.cyberpublicity.com'})
    response = requests.get('https://nickdimakis.com/en/', headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html5lib') # html5lib or lxml

    keywords = ['gtag', 'googletagmanager']
    scripts = soup.find_all('script')
    app.logger.debug(f'scripts: {len(scripts)}')

    for script in scripts:
        script_needs_to_be_removed = False
        script_text = script.string
        script_src = script.attrs.get('src')

        for keyword in keywords:
            if script_text and script_text.lower().find(keyword) > -1:
                app.logger.debug(f'script_text: {script_text}')
                script_needs_to_be_removed = True
                break

            if script_src and script_src.lower().find(keyword) > -1:
                app.logger.debug(f'script_text: {script_src}')
                script_needs_to_be_removed = True
                break

        if script_needs_to_be_removed:
            script.decompose()

    return soup.prettify()


if __name__ == '__main__':
    app.run(debug=True)
