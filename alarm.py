import os
import re
import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

cur_dir = os.path.dirname(os.path.realpath(__file__))
LAST_ID_JSON_FILE_PATH = os.path.join(cur_dir, 'last_id.json')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELETRAM_CHAT_ID = os.getenv('TELETRAM_CHAT_ID')
TELEGRAM_API_SEND_MSG_URI = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

FSC_NEWS_BASE_URL = 'https://www.fsc.go.kr/no010101'
FSC_SEARCH_TEXT = os.getenv('FSC_SEARCH_TEXT')


# Fetch news from yesterday
today = datetime.today()
start_date = (today - timedelta(1)).strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

# https://www.fsc.go.kr/no010101?srchBeginDt=2021-05-31&srchEndDt=2021-06-05&srchKey=all&srchText=%EA%B0%9C%EC%A0%95
news_search_params = {
    'srchBeginDt': start_date,
    'srchEndDt': end_date,
    'srchKey': 'all',
    'srchText': FSC_SEARCH_TEXT
}
response_text = requests.get(FSC_NEWS_BASE_URL, params=news_search_params).text

soup = BeautifulSoup(response_text, 'html.parser')
contents = soup.select('#container > div.content-body > div > div.board-list-wrap > ul > li > div > div.cont > div.subject > a')

# No new content
if not contents:
    exit()

for content in reversed(contents):
    last_id = None

    # Get last_id if exists
    if os.path.exists(LAST_ID_JSON_FILE_PATH):
        with open(LAST_ID_JSON_FILE_PATH, 'r') as json_file:
            json_data = json.load(json_file)
            last_id = int(json_data['last_id'])
    
    news_path = content['href']
    news_id = int(re.findall(r'/(\d+)[?]', news_path)[0])
    news_uri = f'{FSC_NEWS_BASE_URL}/{news_id}'
    news_title = content['title'] #content.string

    # Already sent to Telegram
    if last_id and news_id <= last_id:
        continue

    # Send a message to Telegram
    telegramMessage = f'<b>새로운 보도자료</b>\n\n<pre>{news_title}</pre>\n\n<a href="{news_uri}">보러가기</a>'
    telegram_data = {
        'chat_id': TELETRAM_CHAT_ID,
        'text': telegramMessage,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    requests.post(TELEGRAM_API_SEND_MSG_URI, data=telegram_data)

    # Update last_id with current news_id
    with open(LAST_ID_JSON_FILE_PATH, 'w') as json_file:
        json_data = {
            'last_id': str(news_id)
        }
        json.dump(json_data, json_file)
