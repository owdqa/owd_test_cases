import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        self.test_contact = MockContact()
        self.UTILS.general.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')

    def tearDown(self):
        self.cleanup_storage()
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.create_contact(self.test_contact, "gallery")

        self.contacts.verify_image_in_all_contacts(self.test_contact['name'])
        self.contacts.check_view_contact_details(self.test_contact, True)
