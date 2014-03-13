#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Messages

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        test_str = "Nine 123456789 numbers."
        self.messages.createAndSendSMS([self.num1], test_str)
        x = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Long press the emedded number link.
        #
        y = x.find_element("tag name", "a")  
        y.tap()
        
        #
        # Verufy everything's there.
        #
        fnam = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot (for reference):", fnam)

        self.UTILS.waitForElements(DOM.Messages.header_create_new_contact_btn, "Create new contact button")
        self.UTILS.waitForElements(DOM.Messages.header_add_to_contact_btn, "Add to existing contact button")
        self.UTILS.waitForElements(DOM.Messages.header_cancel_btn_absolute, "Cancel button")

