from google import search
from difflib import SequenceMatcher
import itertools
from newspaper import Article, ArticleException
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NoResultExecption(Exception):
    pass


jj = 'donald-trump-zlikwidowal-nasa'
r = 'przygotował zamach na Putina'
real = 'zamach w Kabulu'


def get_urls_from_search_engine(key_words, num_of_searches):
    list_of_urls = search(key_words, stop=num_of_searches)
    return list_of_urls


def download_article(list_of_urls):
    sities_text = []
    excption_counter = 0
    all_trials = 0
    for url in list_of_urls:
        all_trials += 1
        logger.info(url)
        article = Article(url)
        article.download()
        try:
            article.parse()
            sities_text.append(article.text)
        except ArticleException:
            excption_counter += 1

    if excption_counter == all_trials:
        text = 'cannot parse articles - check internet connection'
        raise NoResultExecption()
    elif excption_counter:
        text = '{} artices has problem with parse'.format(excption_counter)
        logger.warning(text)

    return sities_text


def compare_strings(sities_text):
    sim = []
    for (i, a), (j, b) in itertools.combinations(enumerate(sities_text), 2):
        similarity = SequenceMatcher(None, a, b).ratio()
        sim.append((i, j, similarity))
        text = 'compare result {} with result {} = {}'.format(i, j, similarity)
        logger.debug(text)
    return sim


# convert [(a1, b1, c1), (a2, b2, c2), ...]
# to [(a1, a2, ...), (b1, b2, ...), (c1, c2, ...)]
def rotate_tuple_list(list_of_tuples):
    values = zip(*list_of_tuples)
    x, y, z = values
    for xx, yy, zz in zip(x, y, z):
        print('x: ', xx, ', y: ', yy, ', z: ', zz)
    return values


def plot3d(xpos, ypos, values, num_of_compared_texts):
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')

    def filter_ones(x):
        if x != 1.0:
            return x
        else:
            return 0.0

    size = len(xpos)
    logger.info('size {}'.format(size))

    zpos = np.zeros(size)
    dx = np.ones(size)
    dy = np.ones(size)
    dz = list(map(filter_ones, values))

    div = num_of_compared_texts
    colors = [(g/div, b/div, 1-(g+b)/2/div) for (g, b) in zip(xpos, ypos)]

    for r, g, b in colors:
        logger.debug('r:', r, 'g:', g, 'b:', b)

    ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors)
    plt.show()


def make_analize(key_words, num_of_searches):
    urls = get_urls_from_search_engine(key_words, num_of_searches)
    articles = download_article(urls)
    similar = compare_strings(articles)
    max_similarity = max(similar[2])
    values = rotate_tuple_list(similar)
    plot3d(*values, len(articles))
    return max_similarity

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('key_words', type=str, default=jj,
                        help='key words to find article')
    help = 'Set numbers of articles to find in google search engine'
    parser.add_argument('--num_of_searches', '-n', type=int,
                        default=10, help=help)
    args = parser.parse_args()

    make_analize(args.key_words, args.num_of_searches)

