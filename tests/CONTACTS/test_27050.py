#===============================================================================
# 27050: Cancel while the contact list is being obtained
#
# Procedure:
# 1. Open Contacts app
# 2. Go to Settings
# 3. Tap on Import from Hotmail
# 4. The log in screen is shown
# 5. Introduce a valid user/password
# 6. While the contact list is being obtained, tap Cancel (X icon)
#
# Expected results:
# User should have the possibility to Cancel while the contact list is being
# retrieved.
# User is taken back to Import contacts screen
#===============================================================================

import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.hotmail_user = self.UTILS.general.get_os_variable("HOTMAIL_1_EMAIL")
        self.hotmail_passwd = self.UTILS.general.get_os_variable("HOTMAIL_1_PASS")

        #
        # Get details of our test contacts.
        #
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.connect_to_network()

        self.contacts.launch()

        #
        # Hotmail import selection
        #
        x = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()

        time.sleep(2)

        x = self.UTILS.element.getElement(DOM.Contacts.import_contacts, "Import button")
        x.tap()

        time.sleep(2)

        #
        # Press the Hotmail button.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.hotmail_button, "Hotmail button")
        x.tap()

        #
        # Loggin in
        #
#===============================================================================
#        try:
#            element = "//iframe[contains(@{}, '{}')]".\
#                           format(DOM.Contacts.hotmail_frame[0], DOM.Contacts.hotmail_frame[1])
#
#            self.wait_for_element_present("xpath", element, timeout=5)
#        except:
#            self.UTILS.test.TEST(False, "Already logged in. Cannot continue the test")
#===============================================================================
        #
        # Switch to the hotmail login frame.
        #
        #self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_frame)
        time.sleep(2)
        self.UTILS.element.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")

        #
        # Send the login information (sometimes the username isn't required, just the password).
        # I 'know' that the password field will appear though, so use that element to get the
        # timing right.
        #
        time.sleep(3)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switch_to_frame("")
        self.wait_for_element_displayed(*DOM.Contacts.hotmail_password, timeout=30)
        try:
            self.wait_for_element_displayed(*DOM.Contacts.hotmail_username, timeout=2)

            x = self.marionette.find_element(*DOM.Contacts.hotmail_username)
            x.send_keys(self.hotmail_user)
        except:
            pass

        x = self.UTILS.element.getElement(DOM.Contacts.hotmail_password, "Password field")
        x.send_keys(self.hotmail_passwd)

        #
        # Sign in
        #
        x = self.UTILS.element.getElement(DOM.Contacts.hotmail_signIn_button, "Sign In button")
        x.tap()

        #
        # Cancel the import process
        #
        x = self.UTILS.element.getElement(("id", "popup-close"), "Cancel cross")
        x.tap()

        #
        # Verify we are headed back to "Import contacts" screen
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.element.waitForElements(DOM.Contacts.import_contacts_header, "Import contacts header");
