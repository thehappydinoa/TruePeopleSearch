import random
import time
import webbrowser

import requests
from bs4 import BeautifulSoup
from canari.maltego.message import MaltegoException
from fake_useragent import UserAgent

__author__ = 'thehappydinoa'
__copyright__ = 'Copyright 2018, TruePeopleSearch Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.2'
__maintainer__ = 'thehappydinoa'
__email__ = 'thehappydinoa@gmail.com'
__status__ = 'Development'

session = requests.Session()
ua = UserAgent()


def scrape(url):
    if not url:
        return

    response = session.get(url, headers={"User-Agent": ua.random})

    if "InternalCaptcha" in response.url:
        raise MaltegoException("Internal Captcha: " + response.url)

    if response.status_code == requests.codes.ok:
        return BeautifulSoup(response.content, "html.parser")
    raise MaltegoException(response.status_code)
