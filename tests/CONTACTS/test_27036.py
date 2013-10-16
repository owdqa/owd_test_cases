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
        self.Settings   = Settings(self)

        self.wifi_name  = self.UTILS.get_os_variable("GLOBAL_WIFI_NAME")
        self.wifi_user  = self.UTILS.get_os_variable("GLOBAL_WIFI_USERNAME")
        self.wifi_pass  = self.UTILS.get_os_variable("GLOBAL_WIFI_PASSWORD")

        #
        # Get details of our test contacts.
        #
        self.cont = MockContacts().Contact_1
        self.data_layer.insert_contact(self.cont)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # WIFI.
        #
        self.Settings.launch()

        self.Settings.wifi()
        self.Settings.wifi_switchOn()
        self.Settings.wifi_connect(self.wifi_name, self.wifi_user, self.wifi_pass)
        
        #
        # Launch contacts app.
        #
        self.contacts.launch()
        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()

        x = self.UTILS.getElement(DOM.Contacts.import_contacts, "Import button")
        x.tap()
        
        #
        # Press the Gmail button and go to the gmail frame.
        #
        x = self.UTILS.getElement(DOM.Contacts.gmail_button, "Gmail button")
        x.tap()
        
        self.UTILS.logResult("info", "Check that the gmail login frame is present ...")
        self.marionette.switch_to_frame()
        self.UTILS.waitForElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
                                     (DOM.Contacts.gmail_frame[0],DOM.Contacts.gmail_frame[1])),
                                   "Gmail login iframe")
        x = self.UTILS.getElement(DOM.Contacts.import_cancel_login, "Cancel button")
        x.tap()
        
        self.UTILS.logResult("info", "Check that the gmail login frame is no longer present ...")
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
                                     (DOM.Contacts.gmail_frame[0],DOM.Contacts.gmail_frame[1])),
                                   "Gmail login iframe")

        self.UTILS.logResult("info", "Check that the contacts app is now visible again ...")
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        #
        # Press the cancel icon.
        #
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot and details", x)


