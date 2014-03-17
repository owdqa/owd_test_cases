#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.facebook import Facebook
from OWDTestToolkit.utils import UTILS
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.facebook = Facebook(self)

        #
        # Import details of our test contacts.
        #
        self.contact = MockContact()
        self.UTILS.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        self.UTILS.getNetworkConnection()

        #
        # Launch contacts app and enable facebook import.
        #
        self.contacts.launch()

        self.contacts.tapSettingsButton()

        self.contacts.enable_FB_import()
        fb_user = self.UTILS.get_os_variable("T19180_FB_USERNAME")
        fb_pass = self.UTILS.get_os_variable("T19180_FB_PASSWORD")
        self.facebook.login(fb_user, fb_pass)

        #
        # Import facebook contacts.
        #
        self.contacts.switch_to_facebook()
        self.facebook.importAll()

        #
        # Go back to "All contacts" screen
        #
        backBTN = self.UTILS.getElement(DOM.Contacts.settings_done_button, "Details 'done' button")
        backBTN.tap()

        #
        # View the contact details.
        #
        # self.contacts.launch()
        self.contacts.view_contact(self.contact['name'])

        #
        # Press the link button.
        #
        self.contacts.tapLinkContact()

        #
        # Select the contact to link.
        #
        fb_email = self.UTILS.get_os_variable("T19180_FB_LINK_EMAIL_ADDRESS")

        self.facebook.LinkContact(fb_email)

        #
        # Check we're back at our contact.
        #
        self.UTILS.headerCheck(self.contact['name'])

        #
        # Verify that we're now linked.
        #
        self.contacts.verifyLinked(self.contact['name'], fb_email)
