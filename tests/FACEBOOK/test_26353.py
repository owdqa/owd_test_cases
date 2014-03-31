#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.facebook import Facebook
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.utils import UTILS

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
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Set up a network connection.
        #
        self.UTILS.network.getNetworkConnection()

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Enable facebook and log in.
        #
        self.contacts.tapSettingsButton()
        self.contacts.enable_FB_import()

        fb_user = self.UTILS.general.get_os_variable("T19392_FB_USERNAME")
        fb_pass = self.UTILS.general.get_os_variable("T19392_FB_PASSWORD")
        self.facebook.login(fb_user, fb_pass)

        #
        # Import facebook contacts.
        #
        self.contacts.switch_to_facebook()
        friend_count = self.facebook.importAll()

        #
        # Go back to "All contacts" screen
        #
        backBTN = self.UTILS.element.getElement(DOM.Contacts.settings_done_button, "Details 'done' button")
        backBTN.tap()

        x = self.UTILS.element.getElements(DOM.Contacts.social_network_contacts, "Social network contact list",
                                   True, 20, False)

        self.UTILS.test.TEST(len(x) == friend_count,
                        str(friend_count) + " social network friends listed (there were " + str(len(x)) + ").")

        self.contacts.tapSettingsButton()

        x = self.UTILS.element.getElement(DOM.Facebook.totals, "Facebook totals")
        y = str(friend_count) + "/" + str(friend_count) + " friends imported"
        self.UTILS.test.TEST(x.text == y, "After import, import details = '" + y + "' (it was '" + x.text + "').")
