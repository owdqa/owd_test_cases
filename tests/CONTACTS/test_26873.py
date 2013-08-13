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
        # Get details of our test contacts.
        #
        self.cont1 = MockContacts().Contact_1
        self.cont2 = MockContacts().Contact_2
        self.cont3 = MockContacts().Contact_3
        
        self.nameIncomplete=self.cont1["givenName"][:3]
        self.surnameIncomplete=self.cont1["familyName"][:4]
        
        self.cont2["givenName"]=self.nameIncomplete + "h"
        self.cont2["familyName"]=self.surnameIncomplete + "t"
        
        self.data_layer.insert_contact(self.cont1)
        self.data_layer.insert_contact(self.cont2)
        self.data_layer.insert_contact(self.cont3)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # With nameIncomplete : Search for the sought contact.
        #
        self.contacts.search(self.nameIncomplete)
        
        #
        # With nameIncomplete: Verify our contact is listed.
        #
        self.contacts.checkSearchResults(self.cont1["givenName"])
        self.contacts.checkSearchResults(self.cont2["givenName"])
        
        #
        # With nameIncomplete: Verify the other contact is NOT listed.
        #
        self.contacts.checkSearchResults(self.cont3["givenName"],False)
        
        #
        # Enter one more letter.
        #
        self.UTILS.typeThis(DOM.Contacts.search_contact_input, "Search input", self.cont1["givenName"][3], 
                            p_no_keyboard=True,
                            p_validate=False,
                            p_clear=False,
                            p_enter=False)
        
        #
        # Verify list updated.
        #
        self.contacts.checkSearchResults(self.cont1["givenName"])
        self.contacts.checkSearchResults(self.cont2["givenName"],False)
        self.contacts.checkSearchResults(self.cont3["givenName"],False)
               
        #
        # Cancel search.
        #
        x = self.UTILS.getElement(DOM.Contacts.search_cancel_btn, "Search cancel button")
        x.tap()
                
        #
        # With surnameIncomplete : Search for the sought contact.
        #
        self.contacts.search(self.surnameIncomplete)
        
        #
        # With surnameIncomplete: Verify our contact is listed.
        #
        self.contacts.checkSearchResults(self.cont1["familyName"])
        self.contacts.checkSearchResults(self.cont2["familyName"])
        
        #
        # With surnameIncomplete: Verify the other contact is NOT listed.
        #
        self.contacts.checkSearchResults(self.cont3["familyName"],False)
        
        #
        # Enter one more letter.
        #
        self.UTILS.typeThis(DOM.Contacts.search_contact_input, "Search input", self.cont1["familyName"][4], 
                            p_no_keyboard=True,
                            p_validate=False,
                            p_clear=False,
                            p_enter=False)
        
        #
        # Verify list updated.
        #
        self.contacts.checkSearchResults(self.cont1["familyName"])
        self.contacts.checkSearchResults(self.cont2["familyName"],False)
        self.contacts.checkSearchResults(self.cont3["familyName"],False)