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

import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.settings import Settings
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.settings = Settings(self)

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
        self.UTILS.network.getNetworkConnection()

        #
        # Launch contacts app.
        #
        self.contacts.launch()
        x = self.UTILS.element.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()

        self.wait_for_element_displayed(*DOM.Contacts.import_contacts, timeout=30)
        x = self.UTILS.element.getElement(DOM.Contacts.import_contacts, "Import button")
        x.tap()

        #
        # Wait for the Gmail button.
        #
        self.UTILS.element.waitForElements(DOM.Contacts.gmail_button, "Gmail button")

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot and details", x)
