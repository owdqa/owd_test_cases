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
        self.data_layer.connect_to_cell_data()

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

        self.contacts.hotmail_login(self.hotmail_user, self.hotmail_passwd, True)
        #
        # Cancel the import process
        #
        self.UTILS.reporting.debug("*** Hotmail login complete")
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switch_to_frame("communication")
        self.UTILS.reporting.debug("*** Waiting for curtain to be displayed")
        frame = self.marionette.find_element("id", "fb-curtain")
        self.wait_for_condition(lambda m: "visible" in frame.get_attribute("class"),
                                timeout=30, message="FB Curtain frame was not visible")
        self.marionette.switch_to_frame(frame)
        self.UTILS.reporting.debug("**** Waiting for Cancel button")
        x = self.marionette.find_element("id", "cancel")
        x.tap()

        #
        # Verify we are headed back to "Import contacts" screen
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.element.waitForElements(DOM.Contacts.import_contacts_header, "Import contacts header")
