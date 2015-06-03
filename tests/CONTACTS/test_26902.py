import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

from OWDTestToolkit.utils.contacts import MockContact
from tests.CONTACTS.shared_test_functions import field_remove_toggle


class test_main(field_remove_toggle.field_remove_toggle):

    def test_run(self):
        contact = MockContact()
        self.field_remove_toggle_test(contact, "thumbnail-action")
