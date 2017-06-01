from google import search
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
import itertools
import requests



fake = 'Kryzys w związku. Mąż wrócił wcześniej do domu i przyłapał żonę na kanapie z innym serialem'

real = 'zamach w Kabulu'

list_of_urls = search(real, stop=1)
sities_text = []

def remove(parsed_html, html_tag_list):
    for tag in html_tag_list:
        for to_del in parsed_html.findAll(tag):
            to_del.extract()

for url in list_of_urls:
    print(url)
    html = requests.get(url)
    parsed = BeautifulSoup(html.text, 'html.parser')
    unwanted = ('script', 'a', 'style')
    remove(parsed, unwanted)

    text = parsed.find_all('p')
    sities_text.append(text)
    print(text)
    

sim = []
for (i, a), (j, b) in itertools.combinations(enumerate(sities_text), 2):
    similarity = SequenceMatcher(None, a, b).ratio()
    sim.append((i, j, similarity))

for i, j, val in sim:
    print('compare result ', i, ' with result ', j, ' = ', val)


