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

        #
        # View the contact details.
        #
        self.contacts.viewContact(self.Contact_1['name'])
        
        #
        # Edit the contact.
        #
        self.contacts.pressEditContactButton()
        
        #
        # Check the items.
        #
        self.UTILS.waitForElements(DOM.Contacts.edit_update_button, "Edit 'upate' button")

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Final screenshot", x)