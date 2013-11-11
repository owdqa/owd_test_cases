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

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)
        
        self.num  = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Create a call log.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.callThisNumber()
        time.sleep(2)
        self.dialer.hangUp()
         
        #
        # Open the call log and select Add to Contact.
        #
        self.dialer.openCallLog()

        time.sleep(2)

        self.UTILS.getElement(DOM.Dialer.call_log_edit_btn, "Edit button")

        self.marionette.execute_script("""
        var getElementByXpath = function (path) {
            return document.evaluate(path, document, null, 9, null).singleNodeValue;
        };
        getElementByXpath('//*[@id="call-log-edit-button"]').click();
        """)
        
        #
        # Now tap the number and verify that we're not taken to the menu,
        #
        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % self.num),
                                   "The call log for number %s" % self.num)
        x.tap()
         
        self.UTILS.logResult("info", "Checking the call / etc... buttons are not displayed ...")
        self.UTILS.waitForNotElements(DOM.Dialer.call_log_numtap_call, "Call button")
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Final screenshot", x)
