#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps import Messages
from OWDTestToolkit.apps import Contacts
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
        self.contacts   = Contacts(self)
        
        #
        # Put the phone into airplane mode.
        #
        self.data_layer.set_setting('airplaneMode.enabled', True)
        
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
        self.messages.addNumbersInToField([ self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM") ])

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
