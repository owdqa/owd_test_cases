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
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps import Contacts
from OWDTestToolkit.apps.dialer import Dialer
import time

class test_main(GaiaTestCase):

    test_num = "089123456"
    test_msg = "Testing " + test_num + " number."
    
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Dialer = Dialer(self)
        self.contacts = Contacts(self)
        
        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.UTILS.getNetworkConnection()
        
        #
        # Launch messages app.
        #
        self.messages.launch()
         
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], self.test_msg)
        
        #
        # Wait for the last message in this thread to be a 'received' one
        # and click the link.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(x, "Received a message.", True)
        
        y = x.find_element("tag name", "a")
        y.tap()

        x = self.UTILS.getElement(DOM.Messages.header_call_btn, "Call button")
        x.tap()
        
        time.sleep(5)
        
        #
        # Create a contact from this number.
        #
        self.Dialer.createContactFromThisNum()

        #
        # Make sure the number is automatically in the contact details.
        #        
        x = self.UTILS.getElement(("id", "number_0"), "Mobile number field")
        self.UTILS.TEST(x.get_attribute("value") == self.test_num, 
                        "The correct number is automatically entered in the new contact's number field.")
