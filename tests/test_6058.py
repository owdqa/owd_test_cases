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

class test_6058(GaiaTestCase):
    _Description = "CLONE - Try send a sms creating a new thread while airplane is enabled."
    
    _TestMsg     = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)
        self.messages   = Messages(self)
        
        #
        # Put the phone into airplane mode.
        #
        self.data_layer.set_setting('ril.radio.disabled', True)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
      
        #
        # Open sms app and delete every thread to start a new one
        #
        self.messages.launch()
        self.messages.deleteAllThreads()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()
        
        #
        # Insert the phone number in the To field
        #
        self.messages.addNumberInToField(self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self._TestMsg)
        
        #
        # Click send.
        #
        self.messages.sendSMS()
        
        time.sleep(3)


        #
        # Check that popup appears.
        #
        self.messages.checkAirplaneModeWarning()