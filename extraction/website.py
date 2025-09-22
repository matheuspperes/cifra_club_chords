from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag
from requests import Response

from constants import ENCODING_HTML, SELECTOR_TABS
from process.get_driver import get_driver


def get_url(url: str) -> Optional[Response]:
    try:
        response = requests.get(url)
        response.encoding = ENCODING_HTML
        if response.status_code > 399:
            print(f"Erro ao pesquisar url. Status code: {response.status_code}")
            return None
        return response
    except Exception:  # noqa
        print("Erro na tentativa de pesquisar url")
        return None

def get_keys_ids(response):
    soup = BeautifulSoup(response, "html.parser")
    key = soup.find("a", attrs={"title":"alterar o tom"}) # TODO
    if key:
        original_key = key.text
    pass


def get_html_song(soup):
    try:
        # remove tabs
        for tab in soup.select(SELECTOR_TABS):
            tab.decompose()

        # analyze if the tags with the chords and lyrics are available
        container = soup.find("div", class_="cifra-mono")
        if not container:
            print("Cifra não encontrada")
            return None

        pre_tag = container.find("pre")
        if not pre_tag:
            print("Tag 'pre' da cifra não encontrada")
            return None
        return pre_tag

    except Exception:  # noqa
        print("Erro na tentativa de extrair html")
        return None

def get_song_key(soup) -> str:
    key = soup.find("a", attrs={"title": "alterar o tom"})
    if not key:
        return ''
    return key.get_text()

def get_song_and_artist(soup):
    song_name = soup.select_one('#js-w-content > div.g-1.g-fix.cifra > div.g-side-ad > h1').get_text(strip=True)
    artist_name = soup.select_one('#js-w-content > div.g-1.g-fix.cifra > div.g-side-ad > h2').get_text(strip=True)
    return f"{song_name} - {artist_name}"

def get_song_html_requests(url: str) -> Optional[Tag]:
    response = get_url(url)
    if not response:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    html_song = get_html_song(soup)
    if not html_song:
        return None

    return html_song

def get_song_html_selenium(url: str) -> Optional[tuple[Tag, str, str]]:
    driver = get_driver()
    driver.get(url)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    html_song = get_html_song(soup)
    song_artist_name = get_song_and_artist(soup)
    song_key = get_song_key(soup)

    if not html_song:
        return None

    return html_song, song_artist_name, song_key
