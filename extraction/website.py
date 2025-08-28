from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag
from requests import Response

from constants import ENCODING_HTML, SELECTOR_TABS


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


def get_html_song(response: Response):
    try:
        soup = BeautifulSoup(response.text, "html.parser")

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


def get_song_html(url: str) -> Optional[Tag]:
    response = get_url(url)
    if not response:
        return None

    html_song = get_html_song(response)
    if not html_song:
        return None

    return html_song
