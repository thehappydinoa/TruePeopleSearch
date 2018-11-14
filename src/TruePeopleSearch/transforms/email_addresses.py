import requests
from bs4 import BeautifulSoup
from canari.framework import EnableDebugWindow
from canari.maltego.entities import EmailAddress
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



class EmailAddresses(Transform):
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
                email_addresses = soup.find_all(
                    attrs={"class": "__cf_email__"})
                for email_address in email_addresses:
                    fp = email_address['data-cfemail']
                    r = int(fp[:2], 16)
                    email = ''.join([chr(int(fp[i:i + 2], 16) ^ r)
                                     for i in range(2, len(fp), 2)])
                    response += EmailAddress(email)

        return response

    def on_terminate(self):
        pass
