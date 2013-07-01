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

class test_19187(GaiaTestCase):
    _Description = "[CONTACTS] Remove a contact from the favorites list."

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
        x.tap()
        
        #
        # Go back to view all contacts and check this contact is listed in the
        # 'favourites' section.
        #
        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()
        
        #
        # Check our chap is listed in the group favourites.
        #
        favs = ("xpath", DOM.Contacts.favourites_list_xpath % self.Contact_1['name'].replace(" ", ""))
        self.UTILS.waitForElements(favs,"'" + self.Contact_1['name'] + "' in the favourites list")
        
        #
        # View the contact.
        #
        self.UTILS.logResult("info", "*** Removing contact as a favourite ... ***")        
        self.contacts.viewContact(self.Contact_1['name'])
        
        #
        # Press the favourites button.
        #
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.TEST(x.text == "Remove as Favorite",
                        "Favourite toggle button says 'Remove as Favorite' before contact is removed as a favorite.")
        x.tap()
        time.sleep(2)
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.TEST(x.text == "Add as Favorite",
                        "Favourite toggle button says 'Add as Favorite' after contact is removed as a favorite.")

        #
        # Go back to view all contacts and check this contact is listed in the
        # 'favourites' section.
        #
        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()
        
        #
        # Check our chap is no longer listed in the group favourites.
        #
        favs = ("xpath", DOM.Contacts.favourites_list_xpath % self.Contact_1['name'].replace(" ", ""))
        self.UTILS.waitForNotElements(favs,"'" + self.Contact_1['name'] + "' in the favourites list")
        
