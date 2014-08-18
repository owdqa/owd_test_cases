#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Get details of our test contact.
        #
        self.contact = MockContact()

    def tearDown(self):
        self.cleanup_storage()
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Store our picture on the device.
        #
        self.UTILS.general.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Create our contact.
        #
        self.contacts.create_contact(self.contact, "gallery")

        #
        # Verify our contact.
        #
        self.contacts.verify_image_in_all_contacts(self.contact['name'])
        self.contacts.check_view_contact_details(self.contact, True)
