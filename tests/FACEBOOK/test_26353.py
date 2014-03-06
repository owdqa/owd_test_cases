#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.apps import Contacts
from OWDTestToolkit.apps.facebook import Facebook
from OWDTestToolkit.apps import Settings
from OWDTestToolkit.utils import UTILS

#
# Imports particular to this test case.
#
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
        self.settings = Settings(self)

        #
        # Get details of our test contacts.
        #
        self.contact = MockContact()

        #
        # We're not testing adding a contact, so just stick one
        # into the database.
        #
        self.UTILS.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Set up a network connection.
        #
        self.UTILS.getNetworkConnection()

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Enable facebook and log in.
        #
        self.contacts.tapSettingsButton()
        self.contacts.enableFBImport()

        fb_user = self.UTILS.get_os_variable("T19392_FB_USERNAME")
        fb_pass = self.UTILS.get_os_variable("T19392_FB_PASSWORD")
        self.facebook.login(fb_user, fb_pass)

        #
        # Import facebook contacts.
        #
        self.contacts.switchToFacebook()
        friend_count = self.facebook.importAll()

        #
        # Go back to "All contacts" screen
        #
        backBTN = self.UTILS.getElement(DOM.Contacts.settings_done_button, "Details 'done' button")
        backBTN.tap()

        x = self.UTILS.getElements(DOM.Contacts.social_network_contacts, "Social network contact list",
                                   True, 20, False)

        self.UTILS.TEST(len(x) == friend_count,
                        str(friend_count) + " social network friends listed (there were " + str(len(x)) + ").")

        self.contacts.tapSettingsButton()

        x = self.UTILS.getElement(DOM.Facebook.totals, "Facebook totals")
        y = str(friend_count) + "/" + str(friend_count) + " friends imported"
        self.UTILS.TEST(x.text == y, "After import, import details = '" + y + "' (it was '" + x.text + "').")
