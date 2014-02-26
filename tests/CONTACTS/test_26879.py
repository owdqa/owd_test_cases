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
        self.dialer     = Dialer(self)
    
        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': '+345555555555'})
        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for our new contact.
        #
        self.contacts.viewContact(self.Contact_1["name"])
        
        #
        # Tap the phone number.
        #
        x = self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        x.tap()
        
        #
        # Switch to dialer.
        #
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        
        self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP % self.Contact_1["name"]),
                                    "Outgoing call found with number matching %s" %  self.Contact_1["name"])
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of contact:", x)

