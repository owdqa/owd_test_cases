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
from tests._mock_data.contacts import MockContacts
import time

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
        self.cont = MockContacts().Contact_1
        self.cont["tel"]["value"] = "+34" + self.cont["tel"]["value"] 
        self.data_layer.insert_contact(self.cont)
        
        
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
        self.contacts.viewContact(self.cont["name"])
        
        #
        # Tap the phone number.
        #
        x = self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        x.tap()
        
        #
        # Switch to dialer.
        #
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        
        self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP % self.cont["name"]),
                                    "Outgoing call found with number matching %s" %  self.cont["name"])
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of contact:", x)

        self.dialer.hangUp()        

