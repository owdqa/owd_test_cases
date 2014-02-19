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
        self.Contact_1 = MockContact(givenName = 'Agivenname', familyName = 'Cfamailyname', name = 'Agivenname Cfamailyname')
        self.Contact_2 = MockContact(givenName = 'Bgivenname', familyName = 'Bfamailyname', name = 'Bgivenname Bfamailyname')
        self.Contact_3 = MockContact(givenName = 'Cgivenname', familyName = 'Afamailyname', name = 'Cgivenname Afamailyname')

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
        # Because we don't know what the initial state of the search order is, check it twice.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        if x[0].text != self.Contact_1["name"]:
            self.UTILS.logResult("info", "(NOTE: it looks like the initial search order may need to be changed)")
            self._toggleSearchOrder()

        self.UTILS.logResult("info", "<b>Checking when sorted by given name (first name) ...</b>")
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        self.UTILS.TEST(x[0].text == self.Contact_1["name"], "'%s' is the first contact listed." % self.Contact_1["name"])
        self.UTILS.TEST(x[1].text == self.Contact_2["name"], "'%s' is the second contact listed." % self.Contact_2["name"])
        self.UTILS.TEST(x[2].text == self.Contact_3["name"], "'%s' is the thrid contact listed." % self.Contact_3["name"])
        
        self._toggleSearchOrder()

        self.UTILS.logResult("info", "<b>Checking when sorted by family name (last name) ...</b>")
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        self.UTILS.TEST(x[0].text == self.Contact_3["name"], "'%s' is the first contact listed." % self.Contact_3["name"])
        self.UTILS.TEST(x[1].text == self.Contact_2["name"], "'%s' is the second contact listed." % self.Contact_2["name"])
        self.UTILS.TEST(x[2].text == self.Contact_1["name"], "'%s' is the third contact listed." % self.Contact_1["name"])

    def _toggleSearchOrder(self):
        self.UTILS.logResult("info", "<b>Changing sort order ...</b>")
        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()
        x = self.UTILS.getElement( ("id", "settingsOrder"), "'Order by last name' switch")
        x.tap()
        x = self.UTILS.getElement(DOM.Contacts.settings_done_button, "Done button")
        x.tap()

