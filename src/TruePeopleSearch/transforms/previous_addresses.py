from canari.framework import EnableDebugWindow
from canari.maltego.entities import Location
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


class PreviousAddresses(Transform):
    """Gathers addresses from TruePeopleSearch"""
    input_type = TruePerson

    def do_transform(self, request, response, config):
        person = request.entity
        fields = person.fields

        soup = scrape(fields.get("properties.url"))

        if soup:
            addresses = soup.find_all(
                attrs={"data-link-to-more": "address"})
            for address in addresses:
                response += Location(address.get_text())

        return response

    def on_terminate(self):
        pass
