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
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.hotmail_user = self.UTILS.general.get_config_variable("hotmail_1_email", "common")
        self.hotmail_passwd = self.UTILS.general.get_config_variable("hotmail_1_pass", "common")

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
        settings_btn = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        settings_btn.tap()

        time.sleep(2)

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_contacts, "Import button")
        import_btn.tap()

        time.sleep(2)

        #
        # Press the Hotmail button.
        #
        hotmail_btn = self.UTILS.element.getElement(DOM.Contacts.hotmail_button, "Hotmail button")
        hotmail_btn.tap()

        self.contacts.hotmail_login(self.hotmail_user, self.hotmail_passwd, True)
        #
        # Cancel the import process
        #
        self.marionette.switch_to_frame(self.marionette.find_element("id", "fb-curtain"))
        btn = self.marionette.find_element("id", "cancel")
        btn.tap()

        #
        # Verify we are headed back to "Import contacts" screen
        #
        #self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.element.waitForNotElements(DOM.Contacts.import_import_btn, "Import button")
