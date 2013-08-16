#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *
import time

#
# Imports particular to this test case.
#
from tests._mock_data.contacts import MockContacts

class test_main(GaiaTestCase):
    
    _TestMsg     = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        
        #
        # Prepare the contact.
        #
        self.cont = MockContacts().Contact_1
        self.data_layer.insert_contact(self.cont)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        
        #
        # View the details of our contact and make him a favourite.
        #
        self.contacts.viewContact(self.cont['name'])
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Favourite button")
        x.tap()
        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Favourite button")
        x.tap()
        time.sleep(1)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "(TEST CASE INCOMPLETE, I'M STILL WORKING ON IT - Roy.)", x)


        
        
