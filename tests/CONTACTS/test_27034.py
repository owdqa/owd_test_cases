#===============================================================================
# 27034: Verify that on Contacts going to Settings, there is an option
# to import contacts from Gmail
#
# Procedure:
# 1. Open Contacts app
# 2. Go to Contact settings
# 3. Verify that there is an option to import from gmail
#
# Expected result:
# There should be an option on Contact settings to import contacts
# from gmail. It is presented as well as its icon
#===============================================================================
import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.utils.contacts import MockContact


class test_main(FireCTestCase):

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)
        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        x = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Contacts.import_contacts, "Import button")
        time.sleep(1)
        x.tap()

        self.UTILS.element.waitForElements(DOM.Contacts.gmail_button, "Gmail button")
