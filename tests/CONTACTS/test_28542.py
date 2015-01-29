# OWD-28542:  Verify that the user can cancel a importation from "SD CARD" while it's in process
#
# ** Procedure
#       1. Open contacts app
#       2. Press settings button
#       3. Select import form "SD CARD" option
#       4. Press import button
#       5. Press cancel button while the importation is in process
# ** Expected Results
#       The importation is canceled and any contact that have been imported during the cancelled import
#       session will not be removed. i.e. cancel is 'cancel' and not 'cancel and undo'
#
import time
import os
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        # Export some dummy contacts
        self.initial_population = 10
        self.test_contacts = [MockContact() for i in range(self.initial_population)]
        map(self.UTILS.general.insertContact, self.test_contacts)

        # Delete all previous exportation, just in case
        os.system("adb shell rm sdcard/*.vcf > /dev/null 2>&1")
        self.contacts.launch()
        self.contacts.export_sd_card()

        select_all_btn = self.UTILS.element.getElement(DOM.Contacts.action_select_all, "Select All")
        select_all_btn.tap()
        export_btn = self.UTILS.element.getElement(DOM.Contacts.select_action, "Export button")
        export_btn.tap()
        # Check that there is a layer informing about the success export
        self.UTILS.element.waitForElements(("id", "statusMsg"), "x/y contact exported msg")
        
        self.apps.kill_all()
        time.sleep(2)

        self.contacts.launch()
        self.contacts.delete_all_contacts()
        
        self.test_contact = MockContact()
        self.UTILS.general.insertContact(self.test_contact)
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        settings_btn = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        settings_btn.tap()

        import_btn = self.UTILS.element.getElement(DOM.Contacts.import_contacts, "Import contacts button")
        import_btn.tap()

        import_sd_btn = self.UTILS.element.getElement(DOM.Contacts.import_sd_btn, "Import from SD card button")
        time.sleep(1)
        import_sd_btn.tap()

        cancel_btn = self.UTILS.element.getElement(DOM.GLOBAL.cancel_overlay, "Cancel the import")
        cancel_btn.tap()

        header = self.UTILS.element.getElement(DOM.Contacts.import_contact_header, "Go back btn")
        time.sleep(1)
        header.tap(25, 25)

        settings_done_button = self.UTILS.element.getElement(
            DOM.Contacts.settings_done_button, "Contacts app settings 'done' button")
        time.sleep(1)
        settings_done_button.tap()

        current_contact_number = len(self.marionette.find_elements(*DOM.Contacts.view_all_contact_list))
        self.UTILS.test.test(current_contact_number < self.initial_population,
                             "After cancelling importation, the number of contacts remains the same")
