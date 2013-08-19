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
        
        self.cont1["givenName"]  = "Agivenname"
        self.cont2["givenName"]  = "Bgivenname"
        self.cont3["givenName"]  = "Cgivenname"
        self.cont1["familyName"] = "Cfamailyname"
        self.cont2["familyName"] = "Bfamailyname"
        self.cont3["familyName"] = "Afamailyname"
        
        self.cont1["name"]       = self.cont1["givenName"] + " " + self.cont1["familyName"]
        self.cont2["name"]       = self.cont2["givenName"] + " " + self.cont2["familyName"]
        self.cont3["name"]       = self.cont3["givenName"] + " " + self.cont3["familyName"]
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
        # Because we don't know what the initial state of the search order is, check it twice.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        if x[0].text != self.cont1["name"]:
            self.UTILS.logResult("info", "(NOTE: it looks like the initial search order may need to be changed)")
            self._toggleSearchOrder()

        self.UTILS.logResult("info", "<b>Checking when sorted by given name (first name) ...</b>")
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        self.UTILS.TEST(x[0].text == self.cont1["name"], "'%s' is the first contact listed." % self.cont1["name"])
        self.UTILS.TEST(x[1].text == self.cont2["name"], "'%s' is the second contact listed." % self.cont2["name"])
        self.UTILS.TEST(x[2].text == self.cont3["name"], "'%s' is the thrid contact listed." % self.cont3["name"])
        
        self._toggleSearchOrder()

        self.UTILS.logResult("info", "<b>Checking when sorted by family name (last name) ...</b>")
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        self.UTILS.TEST(x[0].text == self.cont3["name"], "'%s' is the first contact listed." % self.cont3["name"])
        self.UTILS.TEST(x[1].text == self.cont2["name"], "'%s' is the second contact listed." % self.cont2["name"])
        self.UTILS.TEST(x[2].text == self.cont1["name"], "'%s' is the third contact listed." % self.cont1["name"])


    def _toggleSearchOrder(self):
        self.UTILS.logResult("info", "<b>Changing sort order ...</b>")
        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()
        x = self.UTILS.getElement( ("id", "settingsOrder"), "'Order by last name' switch")
        x.tap()
        x = self.UTILS.getElement(DOM.Contacts.settings_done_button, "Done button")
        x.tap()

