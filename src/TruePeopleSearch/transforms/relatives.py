import requests
from bs4 import BeautifulSoup
from canari.framework import EnableDebugWindow
from canari.maltego.entities import Person
from canari.maltego.transform import Transform

from .common.entities import TruePerson

__author__ = 'thehappydinoa'
__copyright__ = 'Copyright 2018, TruePeopleSearch Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'thehappydinoa'
__email__ = 'thehappydinoa@gmail.com'
__status__ = 'Development'



class Relatives(Transform):
    input_type = TruePerson

    def do_transform(self, request, response, config):
        person = request.entity
        fields = person.fields

        user_agent = config['TruePeopleSearch.local.user_agent'].replace(
            '"', "")
        if fields.get("properties.url"):
            r = requests.get(fields.get("properties.url").value,
                             headers={"User-Agent": user_agent})

            if r.status_code == 200:
                page = r.content
                soup = BeautifulSoup(page, "html.parser")
                relatives = soup.find_all(
                    attrs={"data-link-to-more": "relative"})
                for relative in relatives:
                    response += Person(relative.get_text())

        return response

    def on_terminate(self):
        pass