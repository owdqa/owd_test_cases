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

        self.nameIncomplete=self.Contact_1["givenName"][:4]
        self.surnameIncomplete=self.Contact_1["familyName"][:2]

        name2 = self.nameIncomplete + "h"
        fname2 = self.surnameIncomplete + "t"

        self.Contact_2 = MockContact(givenName = name2, familyName = fname2)
        self.Contact_3 = MockContact(givenName = 'John', familyName = 'Smith')
        
        self.UTILS.insertContact(self.Contact_1)
        self.UTILS.insertContact(self.Contact_2)
        self.UTILS.insertContact(self.Contact_3)

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
        self.contacts.checkSearchResults(self.Contact_1["givenName"])
        self.contacts.checkSearchResults(self.Contact_2["givenName"])
        
        #
        # With nameIncomplete: Verify the other contact is NOT listed.
        #
        self.contacts.checkSearchResults(self.Contact_3["givenName"],False)
        
        #
        # Enter one more letter.
        #
        self.UTILS.typeThis(DOM.Contacts.search_contact_input, "Search input", self.Contact_1["givenName"][4],
                            p_no_keyboard=True,
                            p_validate=False,
                            p_clear=False,
                            p_enter=False)
        
        #
        # Verify list updated.
        #
        self.contacts.checkSearchResults(self.Contact_1["givenName"])
        self.contacts.checkSearchResults(self.Contact_2["givenName"],False)
        self.contacts.checkSearchResults(self.Contact_3["givenName"],False)
               
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
        self.contacts.checkSearchResults(self.Contact_1["familyName"])
        self.contacts.checkSearchResults(self.Contact_2["familyName"])
        
        #
        # With surnameIncomplete: Verify the other contact is NOT listed.
        #
        self.contacts.checkSearchResults(self.Contact_3["familyName"],False)
        
        #
        # Enter one more letter.
        #
        self.UTILS.typeThis(DOM.Contacts.search_contact_input, "Search input", self.Contact_1["familyName"][2],
                            p_no_keyboard=True,
                            p_validate=False,
                            p_clear=False,
                            p_enter=False)
        
        #
        # Verify list updated.
        #
        self.contacts.checkSearchResults(self.Contact_1["familyName"])
        self.contacts.checkSearchResults(self.Contact_2["familyName"],False)
        self.contacts.checkSearchResults(self.Contact_3["familyName"],False)