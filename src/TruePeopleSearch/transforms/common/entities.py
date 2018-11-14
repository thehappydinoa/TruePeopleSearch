from canari.maltego.message import *

__author__ = 'thehappydinoa'
__copyright__ = 'Copyright 2018, TruePeopleSearch Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'thehappydinoa'
__email__ = 'thehappydinoa@gmail.com'
__status__ = 'Development'


class TruePerson(Entity):
    _category_ = 'Personal'
    _namespace_ = 'TruePeopleSearch'

    properties_state = StringEntityField('properties.state', display_name='State')
    properties_url = StringEntityField('properties.url', display_name='Url')
    properties_name = StringEntityField('properties.name', display_name='Name', is_value=True)
    properties_zip = IntegerEntityField('properties.zip', display_name='Zip')
    properties_city = StringEntityField('properties.city', display_name='City')
    properties_age = IntegerEntityField('properties.age', display_name='Age')

