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

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.dialer     = Dialer(self)
    
        #
        # Get details of our test contacts.
        #
        self.cont = MockContacts().Contact_1
        self.data_layer.insert_contact(self.cont)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.UTILS.toggleViaStatusBar("airplane")

        #
        # Launch contacts app.
        #
        self.contacts.launch()

        #
        # Search for our new contact.
        #
        self.contacts.viewContact(self.cont["name"])
        
        #
        # Tap the phone number.
        #
        x = self.UTILS.getElement(DOM.Contacts.view_contact_tel_field, "Telephone number")
        x.tap()
        
        #
        # Switch to dialer.
        #
        _warn = self.UTILS.getElement( ("xpath", "//p[contains(text(), 'airplane mode')]"), 
                                    "Airplane mode warning")
        if _warn:
            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("info", "Airplane mode warning displayed: \"%s\"" % _warn.text, x)
        
        x = self.UTILS.getElement( ("xpath", "//button[text()='OK']"), "OK button")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Contacts.view_details_title, "Contact details")

#         self.UTILS.TEST(self.apps.displayed_app.name == "Phone", "The dialer app is now displayed.")


