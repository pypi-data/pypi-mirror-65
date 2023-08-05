import requests
from bs4 import BeautifulSoup

import settings
from logger import logging


def scraper():
    mysettings = settings.config["icecast"]
    soup = url_soup(mysettings["url"])

    trs = soup.select("table.yellowkeys")[0].select("tr")
    info = {}
    for tr in trs:
        k, v = tr.contents
        info[k.text] = " ".join(v.text.split())

    info["now"] = info["Currently playing:"]
    info["hash"] = hash(info["now"])

    return info


def register():
    logging.info("[icecast] reader registered.")
    return scraper


def url_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup
