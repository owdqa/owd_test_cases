import sys
sys.path.insert(1, "./")
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact
from tests.CONTACTS.shared_test_functions import field_remove_toggle


class test_main(field_remove_toggle.field_remove_toggle):

    def test_run(self):
        contact = MockContact(tel=[{'type': 'Mobile', 'value': '555555555'},
                                   {'type': 'Mobile', 'value': '666666666'},
                                   {'type': 'Mobile', 'value': '777777777'}])
        self.field_remove_toggle_test(contact, "contacts-form-phones", [0, 1, 2])
