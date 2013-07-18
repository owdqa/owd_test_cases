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
import time

class test_main(GaiaTestCase):
    
    _TestMsg     = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)
        self.messages   = Messages(self)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Create a new SMS
        #
        self.messages.launch()
        self.messages.startNewSMS()
        
        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([ self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM") ])

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Click send.
        #
        self.messages.sendSMS()
        
        #
        # Wait for the SMS to arrive.
        #
        self.messages.waitForReceivedMsgInThisThread()
        
        time.sleep(10)
        self.marionette.switch_to_frame()
        
        #
        # Put the phone into airplane mode.
        #
        self.UTILS.toggleViaStatusBar('airplane')
        
        #
        # Open sms app and go to the previous thread
        #
        self.messages.launch()
        self.messages.openThread(self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))
        
        #
        # Create another SMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Click send.
        #
        self.messages.sendSMS()

        #
        # Check that popup appears.
        #
        self.messages.checkAirplaneModeWarning()
