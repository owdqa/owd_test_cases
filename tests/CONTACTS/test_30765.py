#===============================================================================
# 30765: Verify that a contact imported from gmail is exported successfully
#
# Procedure:
# 1. Open contacts app
# 2. Press settings button
# 3. Press export contacs button
# 4. Select "To Media Card" option
# 5. Select a Gmail imported contact
# 6. Press export button
#
# Expected result:
# A vcard file is created in the SD card with the contacts exported.
# A temporary layer informing the end user that contacts have been exported
# after finish export process is displayed
#===============================================================================

import os
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.gmail_user = self.UTILS.general.get_config_variable("gmail_1_user", "common")
        self.gmail_passwd = self.UTILS.general.get_config_variable("gmail_1_pass", "common")
        # Set up to use data connection.
        self.connect_to_network()

    def tearDown(self):
        os.system("adb shell rm sdcard/*.vcf")
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd)

        # Log-in in Gmail and contacts imported
        x = self.UTILS.element.getElements(DOM.Contacts.import_conts_list, "Contact list", False)

        gmail_contacts = []
        for y in x:
            contact_name = y.get_attribute("data-search")
            if '#search#' not in contact_name:
                self.UTILS.reporting.logResult("info", "Adding '{}' to the list of available contacts.".\
                                               format(contact_name))
                gmail_contacts.append(contact_name)

        self.contacts.import_all()
        # Saving the number of contacts imported
        self.UTILS.element.waitForElements(("id", "statusMsg"), "x/y contact imported")
        banner = self.UTILS.element.getElement(DOM.Contacts.export_import_banner, "Updated x contacts")
        contacts_imported = banner.text

        # Exit contacts
        self.apps.kill_all()
        time.sleep(2)

        self.contacts.launch()
        self.contacts.export_sd_card()

        select_all_btn = self.UTILS.element.getElement(DOM.Contacts.export_select_all, "Select All")
        select_all_btn.tap()
        time.sleep(2)

        export_btn = self.UTILS.element.getElement(DOM.Contacts.export, "Export button")
        export_btn.tap()

        # Check that there is a layer informing about the success export
        self.UTILS.element.waitForElements(("id", "statusMsg"), "x/y contact exported msg")
        banner = self.UTILS.element.getElement(DOM.Contacts.export_import_banner, "x/y contacts exported")
        contacts_exported = banner.text

        # Check that the number of contact imported/exported is the same
        self.UTILS.reporting.logResult("info", "Contacts imported: {}".format(contacts_imported))
        self.UTILS.reporting.logResult("info", "Contacts exported: {}".format(contacts_exported))
        self.UTILS.test.test(contacts_exported.split("/")[0] in contacts_imported, "OK, same contacts exported than imported")
