#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Contacts
from OWDTestToolkit.apps import Messages


class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        
    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
    
        self.contacts.launch()
        self.messages.launch()
        self.UTILS.touchHomeButton()
        time.sleep(1)
        
        self.UTILS.touchHomeButton()
        
        self.UTILS.switchToFrame(*DOM.Home.frame_locator)
        
        self.UTILS.waitForNotElements( ("xpath", 
                                        "//iframe[contains(@%s,'%s')]" % \
                                        (DOM.Contacts.frame_locator[0],DOM.Contacts.frame_locator[1])),
                                      "Contacts iframe", True, 1)
        
        self.UTILS.waitForNotElements( ("xpath", 
                                        "//iframe[contains(@%s,'%s')]" % \
                                        (DOM.Messages.frame_locator[0],DOM.Messages.frame_locator[1])),
                                      "Messages iframe", True, 1)
        
        self.UTILS.waitForElements( ("xpath", "//div[@class='dockWrapper']"), "Application dock (homescreen)")
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot:", x)