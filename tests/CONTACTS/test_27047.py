#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.settings   = Settings(self)

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact()
        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()

        x = self.UTILS.getElement(DOM.Contacts.import_contacts, "Import button")
        x.tap()

        #
        # Wait for the Hotmail button.
        #
        x = self.UTILS.getElement(DOM.Contacts.hotmail_button, "Hotmail button")
        x_dis = x.get_attribute("disabled")
        self.UTILS.TEST(x_dis == "true", "The Hotmail button is disabled ('disabled' was set to '%s')." % x_dis)
                
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)


