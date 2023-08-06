import bs4
import urllib.request as request
from urllib import parse

from italian_dictionary import exceptions

URL = "https://www.dizionario-italiano.it/dizionario-italiano.php?parola={}"


def build_url(base_url):
    scheme, netloc, path, query, fragment = parse.urlsplit(base_url)
    query = parse.quote(query, safe="?=/")
    return parse.urlunsplit((scheme, netloc, path, query, fragment))  # replacing special characters


def get_soup(url):
    sauce = request.urlopen(url).read()
    soup = bs4.BeautifulSoup(sauce, 'html.parser')
    return soup


def get_lemma(soup):
    lemma = soup.find('span', class_='lemma')
    if lemma is not None:
        return lemma.text
    else:
        raise exceptions.WordNotFoundError()


def get_sillabe(soup, word):
    sillabe = soup.small.span
    if sillabe is not None:
        sillabe = sillabe.string
    else:
        raise exceptions.WordNotFoundError()
    split_indexes = [pos for pos, char in enumerate(sillabe) if char == "|"]
    # necessario perchè le sillabazioni contengono gli accenti di pronuncia
    tmp = list(word)
    for i in split_indexes:
        tmp = tmp[0:i] + ["|"] + tmp[i:]
        sillabe = ''.join(tmp).split("|")
    return sillabe


def get_pronuncia(soup):
    pronuncia = soup.find('span', class_="paradigma")
    return pronuncia.text[10:]


def get_grammatica(soup):
    gram = soup.find_all('span', class_="grammatica")
    return [x.text for x in gram]


def get_locuzioni(soup):
    bad_loc = soup.find_all('span', class_='cit_ita_1')
    loc = [x.text for x in bad_loc]
    return loc


def get_defs(soup):
    defs = []
    for definitions in soup.find_all('span', class_='italiano'):
        children_content = ''
        for children in definitions.findChildren():
            try:
                if children.attrs['class'][0] == 'esempi':
                    continue
                else:
                    children_content += children.text
                    children_content += ' '
                    children.decompose()
            except KeyError:
                children_content += children.text
                children_content += ' '
                children.decompose()
        if children_content != '':
            defs.append(f"{children_content.upper()} -- {definitions.text.replace('()','')}")
        else:
            defs.append(definitions.text)
    if len(defs) == 0:
        raise exceptions.WordNotFoundError()
    return defs


def get_data(word, all_data=True):
    url = build_url(URL.format(word))
    soup = get_soup(url)
    if all_data is False:
        return get_defs(soup)

    data = {'sillabe': get_sillabe(soup, word), 'lemma': get_lemma(soup), 'pronuncia': get_pronuncia(soup),
            'grammatica': get_grammatica(soup), 'definizione': get_defs(soup), 'locuzioni': get_locuzioni(soup),
            'url': url}
    return data
