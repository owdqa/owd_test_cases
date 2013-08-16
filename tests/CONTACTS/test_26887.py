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
        self.UTILS.logResult("info", "<b>Setting up a contact in favourites ...</b>")
        self.contacts.viewContact(self.cont['name'])
        
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        self.UTILS.TEST(x.text == self._addFavStr, "Toggle favourite button text is '%s'." % self._addFavStr)
        x.tap()
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (after tap)")
        self.UTILS.TEST(x.text == self._removeFavStr, "Toggle favourite button text is '%s'." % self._removeFavStr)
        
        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()
        
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.favourites_list_xpath % self.cont["name"].replace(" ", "")),
                                    "%s in favorites" % self.cont["name"])
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)


        
        self.UTILS.logResult("info", "<b>removing contact from favourites ...</b>")
        self.contacts.viewContact(self.cont['name'])
        
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        self.UTILS.TEST(x.text == self._removeFavStr, "Toggle favourite button text is '%s'." % self._removeFavStr)
        x.tap()
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (after tap)")
        self.UTILS.TEST(x.text == self._addFavStr, "Toggle favourite button text is '%s'." % self._addFavStr)
        
        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()
        
        time.sleep(1)
        self.UTILS.waitForNotElements( ("xpath", DOM.Contacts.favourites_list_xpath % self.cont["name"].replace(" ", "")),
                                    "%s in favorites" % self.cont["name"])
        
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)

        
        

        
        
