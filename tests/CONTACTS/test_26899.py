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
                
        #
        # Import details of our test contacts.
        #
        self.Contact_1 = MockContacts().Contact_1
        self.data_layer.insert_contact(self.Contact_1)
    
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # View our contact.
        #
        self.contacts.viewContact(self.Contact_1['name'])
           
        #
        # Edit our contact.
        #
        self.contacts.pressEditContactButton()
         
        #
        # Delete our contact.
        #
        self.contacts.pressDeleteContactButton()
         
        #
        # Cancel deletion.
        #
        x = self.UTILS.getElement(DOM.Contacts.cancel_delete_btn, "Cancel button")
        x.tap()

        x = self.UTILS.getElement(DOM.Contacts.edit_cancel_button, "Cancel edit contact")
        x.tap()

        #
        # Relaunch the app.
        #
        self.contacts.launch()
         
        #
        # Now actually delete our contact.
        #
        self.contacts.deleteContact(self.Contact_1['name'])
 
