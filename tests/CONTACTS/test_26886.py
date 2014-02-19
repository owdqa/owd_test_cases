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
        # Press the favourites button.
        #
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Favourite toggle button")
        self.UTILS.TEST(x.text == "Add as Favorite",
                        "Favourite 'toggle' button is labelled 'Add as Favourite'.")
        x.tap()

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
        
        string = '' + self.Contact_1['familyName'] + self.Contact_1['givenName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath % string)
        self.UTILS.waitForElements(favs,"'" + self.Contact_1['name'] + "' in the favourites list")