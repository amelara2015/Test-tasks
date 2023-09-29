#google colab:
#https://colab.research.google.com/drive/1vm1GSIkcQdRKEcCcV6ewah9JU619mnnD?usp=sharing

import requests
from bs4 import BeautifulSoup
import json
import time
import matplotlib.pyplot as plt
from wordcloud import WordCloud

title_list = []
text_list = []

page = 0
while True: 
  
  url = f'https://m.dzen.ru/news/search?ajax=1&filter_date=1693256400000,1695934800000&flat=30&issue_tld=ru&neo_parent_id=1695960744396136-7803543852703654221-sycyvgck5huo7ujc-BAL-5312-NEWS-NEWS_NEWS_SEARCH&p={page}&sortby=date&text=игра date:20230829..20230929'
  response = requests.post(url)
  soup = BeautifulSoup(response.text, "html.parser")
  response_json = json.loads(soup.text)['data']

  for page_json in response_json['stories']:
    title_list.append("".join([t['text'] for t in page_json['docs'][0]['title']]))
    text_list.append("".join([t['text'] for t in page_json['docs'][0]['text']]))

  if len(response_json['stories']) == 0:
    break
  
  page += 1
  time.sleep(1)

print(f'страниц: {page}, новостей: {len(text_list)}')
# делаем единый текст из новостей. заголовки новостей не используем.
text = " ".join(text_list)


wordCloud = WordCloud(width = 1000, height = 600, random_state=42, background_color='white', colormap='Set1').generate(text)

plt.figure()
plt.axis('off')
plt.imshow(wordCloud)
plt.savefig('game.png', format='png')