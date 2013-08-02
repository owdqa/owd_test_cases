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
    
    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.settings   = Settings(self)

        self.gmail_u = self.UTILS.get_os_variable("GMAIL_1_USER")
        self.gmail_p = self.UTILS.get_os_variable("GMAIL_1_PASS")

        #
        # Get details of our test contacts.
        #
        self.cont = MockContacts().Contact_1
        self.data_layer.insert_contact(self.cont)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Set up to use data connection.
        #
        self.UTILS.getNetworkConnection()
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        self.contacts.import_GmailLogin(self.gmail_u, self.gmail_p, False)
        
        #
        # Cancel the login.
        #
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.Contacts.import_cancel_login, "Cancel icon")
        x.tap()
        
        #
        # Verify that the gmail frame is closed.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
                                        (DOM.Contacts.gmail_frame[0], DOM.Contacts.gmail_frame[1])),
                                      "Gmail login frame")
        
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        self.UTILS.waitForElements( ("xpath", "//h1[text()='Settings']"), "Settings header")
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)


