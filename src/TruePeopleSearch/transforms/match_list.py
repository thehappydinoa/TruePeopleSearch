import requests
from bs4 import BeautifulSoup
from canari.framework import EnableDebugWindow
from canari.maltego.entities import Alias, Person
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



class MatchList(Transform):
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
        user_agent = config['TruePeopleSearch.local.user_agent'].replace(
            '"', "")
        r = requests.get(
            base_url + path, headers={"User-Agent": user_agent})
        if r.status_code == 200:
            # print(r.url)
            page = r.content
            soup = BeautifulSoup(page, "html.parser")

            addresses = soup.find_all(class_="card-summary")
            for t in addresses:
                content = t.find_all(class_="content-value")
                try:
                    age = int(content[0].get_text())
                except:
                    age = 0
                location = content[1].get_text()
                if ", " in location:
                    location_list = location.split(", ")
                    city = location_list[0]
                    state = location_list[1]
                else:
                    city = None
                    state = None
                response += TruePerson(name + " " + location, properties_url=base_url +
                                       t['data-detail-link'], properties_city=city, properties_state=state, properties_age=age)

        return response

    def on_terminate(self):
        pass
