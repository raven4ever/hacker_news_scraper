import pprint

import requests
from bs4 import BeautifulSoup


def sort_stories_by_votes(news_list):
    return sorted(news_list, key=lambda news: news['votes'], reverse=True)


def create_hn_list_by_votes(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


response_first_page = requests.get('https://news.ycombinator.com/news')
response_second_page = requests.get('https://news.ycombinator.com/news?p=2')
soup_first_page = BeautifulSoup(response_first_page.text, 'html.parser')
soup_second_page = BeautifulSoup(response_second_page.text, 'html.parser')

links_first_page = soup_first_page.select('.storylink')
links_second_page = soup_second_page.select('.storylink')
subtext_first_page = soup_first_page.select('.subtext')
subtext_second_page = soup_second_page.select('.subtext')

all_links = links_first_page + links_second_page
all_subtext = subtext_first_page + subtext_second_page

pprint.pprint(create_hn_list_by_votes(all_links, all_subtext))
