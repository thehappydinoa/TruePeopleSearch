from canari.framework import EnableDebugWindow
from canari.maltego.entities import Person
from canari.maltego.transform import Transform

from .common.entities import TruePerson
from .common.scrapper import scrape

__author__ = 'thehappydinoa'
__copyright__ = 'Copyright 2018, TruePeopleSearch Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.2'
__maintainer__ = 'thehappydinoa'
__email__ = 'thehappydinoa@gmail.com'
__status__ = 'Development'


class Match(Transform):
    """Gathers people from TruePeopleSearch"""
    input_type = Person

    def do_transform(self, request, response, config):
        person = request.entity
        fields = person.fields
        name = person.fullname
        citystatezip = []
        for key in ["properties.city", "properties.state", "properties.zip"]:
            value = fields.get(key)
            if value and not str(value.value) == "0":
                citystatezip.append(value.value.strip())

        if citystatezip:
            citystatezip = ",%20".join(citystatezip)
            path = "/results?name=%s&citystatezip=%s" % (name, citystatezip)
        else:
            path = "/results?name=" + name.replace(" ", "%20")

        base_url = config['TruePeopleSearch.local.base_url']

        soup = scrape(base_url + path)

        if soup:
            cards = soup.find_all(class_="card-summary")
            for card in cards:
                card_name = card.find(class_="h4").get_text().strip()
                card_content = card.find_all(class_="content-value")

                age = card_content[0].get_text()
                if "Unknown" in age:
                    age = 0
                elif "(age " in age:
                    age = int(age.split("(age ")[1].replace(")", ""))
                else:
                    age = int(age)

                location = card_content[1].get_text()
                if ", " in location:
                    location_list = location.split(", ")
                    city = location_list[0]
                    state = location_list[1]
                else:
                    city = location
                    state = ""

                response += TruePerson(card_name, properties_url=base_url +
                                       card['data-detail-link'], properties_city=city, properties_state=state, properties_age=age)

        return response

    def on_terminate(self):
        pass
