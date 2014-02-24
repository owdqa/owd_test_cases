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
from tests._mock_data.contacts import MockContact


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
        
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': self.num1})

        self.UTILS.insertContact(self.Contact_1)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        self.contacts.launch()
        self.contacts.viewContact(self.Contact_1["name"])
        x = self.UTILS.getElement(DOM.Contacts.sms_button, "SMS button")
        x.tap()
        
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)

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
