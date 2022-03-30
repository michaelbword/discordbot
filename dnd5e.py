from bs4 import BeautifulSoup
from requests import get


class DnD5e:
    def __init__(self):
        self.headers = None
        self.url = 'http://dnd5e.wikidot.com/'

    def key_words_search_words(self, user_message):
        words = user_message.split()[1:]
        keywords = '+'.join(words)
        search_words = ' '.join(words)
        return keywords, search_words

    def search(self, keywords):
        response = get(self.url + keywords, headers=self.headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        result_links = soup.findAll('a')
        return result_links

    def send_link(self, result_links, search_words):
        send_link = set()
        for link in result_links:
            text = link.text.lower()
            if search_words in text:
                send_link.add(link.get('href'))
        return send_link
