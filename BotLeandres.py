import requests
import time
import optparse
import datetime
import json
import pause
import schedule
import sys
import telegram
import urllib.request
import os
import filecmp
import random
import difflib

from bs4 import BeautifulSoup 
from os.path import exists

list_2 = ['😎', '🥳', '🥸', '🤯', '🥵']
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
days = 0

while True:

    def page(session):

        headers = {
        
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'www.leandres.paris',
        'If-None-Match': 'W/"2b3a9ea196ea47c86da5e43ef9177a72-gzip"',
        'Referer': 'https://www.leandres.paris/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Brave";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

        }

        return session.get('https://www.leandres.paris/shopleandres.html', headers=headers)


    def compute_diff(old_text, new_text):
        diff = difflib.unified_diff(
            old_text.split('\n'),
            new_text.split('\n'),
            fromfile='old',
            tofile='new',
            lineterm='',
        )
        res = '\n'.join(diff)
        return res[34:]

    def notify_change(old_text, new_text):
        
        emoji_h = random.sample(list_2, 1)
        res = compute_diff(old_text, new_text)
        subject=f'[UMLSVP] Mise à jour {emoji_h.pop()} : \n{res}'
        requests.post("https://ntfy.sh/XXXX", data=subject.encode(encoding='utf-8'))

    def notify_change_days(days):

        emoji_h = random.sample(list_2, 1)
        subject=f'{days} jours sans nouvelles du ☕️ Léandrès {emoji_h.pop()}'
        requests.post("https://ntfy.sh/XXXX", data=subject.encode(encoding='utf-8'))

    #STARTING HERE

    session = requests.Session()

    first = page(session)


    emoji_h = random.sample(list_2, 1)
    subject=f'[UMLSVP] Running ✅ {emoji_h.pop()}'
    requests.post("https://ntfy.sh/XXXX", data=subject.encode(encoding='utf-8'))

    soup = BeautifulSoup(first.text, "html.parser")

    content = ""
    for script in soup(['style', 'script']):
        script.extract()

    for text in soup(['h2']):
        content += str(text.get_text()) + '\n'

    file_path = os.path.join(ROOT_DIR,'BotLeandres', 'data','UMLSVP.txt'.format())

    try:
        with open(file_path, 'r') as f:
            old_text = f.read()

    except FileNotFoundError:
        with open(file_path, 'w') as f:
            f.write(content)
            old_text = ''
            emoji_h = random.sample(list_2, 1)
            subject=f'[UMLSVP] New file extract ✅ {emoji_h.pop()}'
            requests.post("https://ntfy.sh/XXXX", data=subject.encode(encoding='utf-8'))

    file_exists = exists(file_path)
    if file_exists:
        if content != old_text:
            days = 0
            notify_change(new_text=content, old_text=old_text)
            with open(file_path, 'w') as f:
                f.write(content)
        else:
            notify_change_days(days)
            days += 1
    
    time.sleep(86400)




