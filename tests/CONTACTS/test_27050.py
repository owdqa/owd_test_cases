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
    
    _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.settings   = Settings(self)

        self.hotmail_u = self.UTILS.get_os_variable("HOTMAIL_1_EMAIL")
        self.hotmail_p = self.UTILS.get_os_variable("HOTMAIL_1_PASS")

        #
        # Get details of our test contacts.
        #
        self.Contact_1 = MockContact()
        self.UTILS.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Set up to use data connection.
        #
        self.UTILS.getNetworkConnection()
        
        self.contacts.launch()

        x = self.contacts.import_HotmailLogin(self.hotmail_u, self.hotmail_p, p_clickSignIn=False)
        x = self.UTILS.getElement(DOM.Contacts.hotmail_signIn_button, "Sign In button")
        x.tap()
        
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.switchToFrame("id", "fb-curtain", p_viaRootFrame=False)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        time.sleep(1)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        time.sleep(1)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        time.sleep(1)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
        
        time.sleep(1)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot at this point:", x)
