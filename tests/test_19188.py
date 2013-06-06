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
from tests.mock_data.contacts import MockContacts
import time

class test_19188(GaiaTestCase):
    _Description = "[CONTACTS] Configure a contact as a favourite."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
                
        #
        #

        #
        # Get details of our test contacts.
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
        # View the contact details.
        #
        self.contacts.viewContact(self.Contact_1['name'])
        
        #
        # Press the favourites button.
        #
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.TEST(x.text == "Add as Favorite",
                        "Favourite 'toggle' button is labelled 'Add as Favourite'.")
        x.tap()
        
        #
        # Verify this contact now has a star in the name.
        #
        self.UTILS.waitForElements(DOM.Contacts.favourite_marker, "Favourite 'marker' beside header name")
        
        #
        # Verify the favourite toggle button label changes correctly.
        #
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.TEST(x.text == "Remove as Favorite",
                        "Favourite 'toggle' button is labelled 'Remove as Favourite'.")
        
        
        #
        # Go back to view all contacts and check this contact is listed in the
        # 'favourites' section.
        #
        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()
        
        favs = ("xpath", DOM.Contacts.favourites_list_xpath % self.Contact_1['name'].replace(" ", ""))
        x = self.UTILS.waitForElements(favs,"'" + self.Contact_1['name'] + "' in the favourites list")
        
