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
from OWDTestToolkit.apps import Contacts
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.contacts   = Contacts(self)
        self.messages   = Messages(self)
        
        #
        # Establish which phone number to use and set up the contacts.
        #
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num2 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")
        self.Contact_1 = MockContact(tel = {'type': 'Mobile', 'value': self.num1})
        self.Contact_2 = MockContact(tel = {'type': 'Mobile', 'value': self.num2})

        self.UTILS.insertContact(self.Contact_1)
        self.UTILS.insertContact(self.Contact_2)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # First, we need to make sure there are no statusbar notifs.
        #
        self.UTILS.clearAllStatusBarNotifs()
        
        #
        # Now create and send an sms to both contacts.
        #
        self.messages.launch()
        self.messages.startNewSMS()
        
        self.messages.selectAddContactButton()
        self.contacts.viewContact(self.Contact_1["name"], False)
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.checkIsInToField(self.Contact_1["name"], True)
        
        self.messages.selectAddContactButton()
        self.contacts.viewContact(self.Contact_2["name"], False)
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.checkIsInToField(self.Contact_2["name"], True)

        self.messages.enterSMSMsg("Test message.")
        self.messages.sendSMS()
        
        #
        # Wait for all statusbar notifs to arrive.
        # Because both sms's are to this device (via different numbers), both
        # messages will probably end up going to the same thread. So just do a count
        # based on the contact with the short number (since this is the one
        # it always comes to).
        #
        self.marionette.switch_to_frame()
        statusBarCheck = (DOM.Messages.statusbar_new_sms[0], 
                          DOM.Messages.statusbar_new_sms[1] % self.Contact_1["name"])
        
        # Loop for 2 minutes (the 2nd one can take a long time!).
        boolOK = False
        for i in range(1,120):
            # No verification because it's okay if the element's not there yet.
            try:
                self.wait_for_element_present(*statusBarCheck, timeout=1)
                x = self.marionette.find_elements(*statusBarCheck)
                if len(x) == 2:
                    boolOK = True
                    break
            except:
                pass
            
            time.sleep(1)
            
        self.UTILS.TEST(boolOK, "Two messages were returned for this device within 2 minutes (there were " + str(len(x)) + ").")
