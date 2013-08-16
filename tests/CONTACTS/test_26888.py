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
        self.cont2 = MockContacts().Contact_1
        self.cont  = MockContacts().Contact_2
        self.cont3 = MockContacts().Contact_3
        self.data_layer.insert_contact(self.cont)
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
        # View the details of our contact and make him a favourite.
        #
        self.UTILS.logResult("info", "<b>Setting up a contact in favourites ...</b>")
        self.contacts.viewContact(self.cont['name'])
        
        x = self.UTILS.getElement(DOM.Contacts.favourite_button, "Toggle favourite button (before tap)")
        x.tap()
        x = self.UTILS.getElement(DOM.Contacts.details_back_button, "Back button")
        x.tap()
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.favourites_list_xpath % self.cont["name"].replace(" ", "")),
                                    "%s in favorites" % self.cont["name"])
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point", x)

        #
        # Now check the favourites list appears first.
        #
        x = self.UTILS.getElements( ("tag name", "ol"), "Contact lists")
        fav_id      = "contacts-list-favorites"
        normal_ids  = "contacts-list-"
        foundFav    = False
        foundNormal = False
        for i in x:
            if fav_id in i.get_attribute("id"):
                foundFav = True
            if normal_ids in i.get_attribute("id"):
                foundNormal = True
                break
                
        self.UTILS.TEST(foundNormal , "Found the non-favourite lists.")
        self.UTILS.TEST(foundFav    , "Found the favourite lists before the non-favourite lists.")
        
        
        