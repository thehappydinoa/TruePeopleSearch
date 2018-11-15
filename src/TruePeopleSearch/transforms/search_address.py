from canari.framework import EnableDebugWindow
from canari.maltego.entities import EmailAddress, Location, PhoneNumber
from canari.maltego.transform import Transform

from .common.entities import TruePerson
from .common.scrapper import scrape

__author__ = 'thehappydinoa'
__copyright__ = 'Copyright 2018, TruePeopleSearch Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'thehappydinoa'
__email__ = 'thehappydinoa@gmail.com'
__status__ = 'Development'


@EnableDebugWindow
class SearchAddress(Transform):
    """Gathers people from TruePeopleSearch"""
    input_type = Location

    def do_transform(self, request, response, config):
        location = request.entity
        fields = location.fields

        if fields.get("streetaddress"):
            name = fields.get("streetaddress").value
        else:
            name = fields.get("location.name").value

        if fields.get("location.areacode"):
            citystatezip = fields.get("location.areacode").value.split("-")[0]
        elif fields.get("city") and fields.get("location.area"):
            citystatezip = fields.get("city").value + \
                ", " + fields.get("location.area").value
        else:
            citystatezip = name.split(" ")[-1].split("-")[0]

        name = name.replace(" ", "%20").replace("\n", "%20")

        path = "/results?streetaddress=%s&citystatezip=%s" % (
            name, citystatezip)

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
