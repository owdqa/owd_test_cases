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

class test_6057(GaiaTestCase):
    _Description = "CLONE - Try send a sms to a phone number (no contact) while airplane is enabled"
    
    _TestMsg     = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)
        self.messages   = Messages(self)
        self.contacts   = Contacts(self)
        
        #
        # Put the phone into airplane mode.
        #
        self.data_layer.set_setting('ril.radio.disabled', True)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
      
        #
        # Open sms app 
        #
        self.messages.launch()
        
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