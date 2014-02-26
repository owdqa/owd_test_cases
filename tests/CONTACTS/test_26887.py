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
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
    _addFavStr      = "Add as Favorite"
    _removeFavStr   = "Remove as Favorite"

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
        # View the details of our contact and make him a favourite.
        #
        self.UTILS.logResult("info", "<b>Setting up a contact in favourites ...</b>")
        self.contacts.viewContact(self.Contact_1['name'])
        
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        self.UTILS.TEST(x.text == self._addFavStr, "Toggle favourite button text is '%s'." % self._addFavStr)
        x.tap()
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (after tap)")
        self.UTILS.TEST(x.text == self._removeFavStr, "Toggle favourite button text is '%s'." % self._removeFavStr)
        
        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()
        
        string = self.Contact_1['givenName'] + self.Contact_1['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath % string)
        self.UTILS.waitForElements(favs,"'" + self.Contact_1['name'] + "' in the favourites list")
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)

        self.UTILS.logResult("info", "<b>removing contact from favourites ...</b>")
        self.contacts.viewContact(self.Contact_1['name'])
        
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        self.UTILS.TEST(x.text == self._removeFavStr, "Toggle favourite button text is '%s'." % self._removeFavStr)
        x.tap()
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (after tap)")
        self.UTILS.TEST(x.text == self._addFavStr, "Toggle favourite button text is '%s'." % self._addFavStr)
        
        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()
        
        time.sleep(1)
        string = self.Contact_1['givenName'] + self.Contact_1['familyName']
        favs = ("xpath", DOM.Contacts.favourites_list_xpath % string)
        self.UTILS.waitForNotElements(favs,"'" + self.Contact_1['name'] + "' in the favourites list")

        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)