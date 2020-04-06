import pprint

import requests
from bs4 import BeautifulSoup


def get_all_articles_from_pages(no_pages):
    all_links = []
    all_subtext = []
    for page in range(no_pages):
        response = requests.get(
            'https://news.ycombinator.com/news?p=' + str(page))
        soup_page = BeautifulSoup(response.text, 'html.parser')
        all_links.extend(soup_page.select('.storylink'))
        all_subtext.extend(soup_page.select('.subtext'))
    return all_links, all_subtext


def sort_stories_by_votes(news_list):
    return sorted(news_list, key=lambda news: news['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 149:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


if __name__ == '__main__':
    all_links, all_subtext = get_all_articles_from_pages(3)

    pprint.pprint(create_custom_hn(all_links, all_subtext))
