#===============================================================================
# 27053: Tap on Unselect All to unselect all the contacts
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
# 7. Once the list of contacts is shown, select some of them
# 8. Then tap on Unselect all (ER1)
# 9. Now tap on Select all option and then on Unselect all again (ER2)
#
# Expected results:
# ER1. All contacts previously selected should be unselected at once
# ER2. All contacts previously selected should be unselected at once
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.contacts import MockContact
import time


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
        self.UTILS.test.test(import_btn.get_attribute("disabled") == "true", "Import button is disabled.")

        #
        # Tap the Select All button (can't be done with marionette yet).
        #
        self.UTILS.reporting.logResult("info", "Tapping the 'Select All' button ...")
        self.marionette.execute_script("document.getElementById('{}').click()".\
                                       format(DOM.Contacts.import_select_all[1]))
        time.sleep(1)

        result = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", result)

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.test(import_btn.get_attribute("disabled") != "true", "Import button is enabled.")

        #
        # The only way I can see to test that all contacts are selected is to toggle
        # all of them and make sure the Import button is then disabled (because that
        # means all of them were selected before the toggle).
        #
        contact_list = self.UTILS.element.getElements(("class name", "block-item"), "Contacts list")
        for i in range(len(contact_list)):
            i_num = i + 1
            self.UTILS.reporting.logResult("info", "Disable contact {} ...".format(i_num))
            self.contacts.import_toggle_select_contact(i_num)

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_import_btn, "Import button")
        self.UTILS.test.test(import_btn.get_attribute("disabled") == "true", "Import button is disabled.")

        result = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", result)
