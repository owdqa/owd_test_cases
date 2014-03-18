#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
import os
import time


class test_main(GaiaTestCase):
    #_RESTART_DEVICE=True
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.gmail_user = self.UTILS.get_os_variable("GMAIL_1_USER")
        self.gmail_passwd = self.UTILS.get_os_variable("GMAIL_1_PASS")

    def tearDown(self):
        self.UTILS.reportResults()
        #Contacts exported to SD Card are removed
        os.system("adb shell rm sdcard/*.vcf")

    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.UTILS.getNetworkConnection()

        self.contacts.launch()
        self.contacts.import_gmail_login(self.gmail_user, self.gmail_passwd)

        #
        #Log-in in Gmail and contacts imported
        #
        x = self.UTILS.getElements(DOM.Contacts.import_conts_list, "Contact list", False)

        gmail_contacts = []
        for y in x:
            contact_name = y.get_attribute("data-search")
            if '#search#' not in contact_name:
                self.UTILS.logResult("info", "Adding '{}' to the list of available contacts.".format(contact_name))
                gmail_contacts.append(contact_name)

        self.contacts.import_all()
        #Saving the number of contacts imported
        self.UTILS.waitForElements(("id", "statusMsg"), "x/y contact imported")
        y = self.UTILS.getElement(DOM.Contacts.export_import_banner, "Updated x contacts")
        self.UTILS.logResult("info", y.text)
        contacts_imported = y.text

        #Exit contacts
        self.apps.kill_all()

        self.contacts.launch()

        #
        #Exporting to SD Card
        #
        self.contacts.export_sd_card()

        x = self.UTILS.getElement(DOM.Contacts.export_select_all, "Select All")
        x.tap()
        time.sleep(2)

        x = self.UTILS.getElement(DOM.Contacts.export, "Export button")
        x.tap()

        #Check that there is a layer informing about the success export
        self.UTILS.waitForElements(("id", "statusMsg"), "x/y contact exported")
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)

        x = self.UTILS.getElement(DOM.Contacts.export_import_banner, "x/y contacts exported")

        contacts_exported = x.text
        #Check that the number of contact imported/exported is the same
        self.UTILS.logResult("info", contacts_exported[0])
        self.UTILS.logResult("info", contacts_imported[8])

        if contacts_imported[8] == contacts_exported[0]:
            self.UTILS.logResult("info", "OK same contacts imported than exported")
        else:
            self.UTILS.quitTest("Different contacts exported than imported")
