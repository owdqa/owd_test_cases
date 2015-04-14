from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)

        #
        # Create test contact.
        #
        self.contact = MockContact()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Create our contact.
        #
        self.contacts.create_contact(self.contact)

        #
        # Verify our contact details.
        #
        self.contacts.check_view_contact_details(self.contact)
