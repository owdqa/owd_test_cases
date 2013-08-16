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
        self.cont = MockContacts().Contact_1
        self.data_layer.insert_contact(self.cont)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.contacts.launch()
        self.contacts.viewContact(self.cont['name'])
        self.contacts.pressEditContactButton()
        
        self.marionette.execute_script("document.getElementById('delete-contact').scrollIntoView();")
        self.marionette.execute_script("document.getElementById('contact-form-title').scrollIntoView();")

        x = self.UTILS.getElement(DOM.Contacts.delete_contact_btn, "Delete contact button")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Contacts.confirm_delete_btn, "Confirmation button")
        y = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", y)
        x.tap()
        
        self.UTILS.waitForElements( ("xpath", "//p[text()='No contacts']"), "'No contacts' message")
        y = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", y)
