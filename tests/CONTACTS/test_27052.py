#===============================================================================
# 27052: Select one (several) contact(s) and verify that the Import option
# is enabled
#
# Pre-requisites:
# To have a Hotmail account with several contacts available to show/import
#
# Procedure:
# 1. Open Contacts app
# 2. Go to Settings
# 3. Tap on Import from Hotmail
# 4. The log in screen is shown
# 5. Introduce a valid user/password
# 6. Tap on Sign In
# 7. Once the list of contacts is shown select one and then several contacts
#
# Expected results:
# The Import option should be disabled till one or several contacts are selected
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

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
        login_result = self.contacts.import_hotmail_login(self.hotmail_user, self.hotmail_passwd)
        if not login_result:
            self.UTILS.reporting.logResult(False, "Cannot continue past this point without importing the contacts.")
            return

        #
        # Check the Import button is disabled to begin with.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.hotmail_import_frame, via_root_frame=False)
        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.TEST(import_btn.get_attribute("disabled") == "true", "Import button is disabled.")

        #
        # Select / de-select contacts and make sure Import button is enabled / disabled
        # as expected.
        #
        self.UTILS.reporting.logResult("info", "Enable contact 1...")
        self.contacts.import_toggle_select_contact(1)

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.TEST(import_btn.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.reporting.logResult("info", "Enable contact 2...")
        self.contacts.import_toggle_select_contact(2)

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.TEST(import_btn.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.reporting.logResult("info", "Disable contact 2...")
        self.contacts.import_toggle_select_contact(2)

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.TEST(import_btn.get_attribute("disabled") != "true", "Import button is enabled.")

        self.UTILS.reporting.logResult("info", "Disable contact 1...")
        self.contacts.import_toggle_select_contact(1)

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.TEST(import_btn.get_attribute("disabled") == "true", "Import button is disabled.")

        result = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", result)
