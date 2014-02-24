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
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):
    
    _TestMsg     = "Test message."
    
    _RESTART_DEVICE= True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
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
        # Launch messages app.
        #
        self.messages.launch()
         
        #
        # Send a message to myself (long and short number to get a few threads).
        #
        self.messages.createAndSendSMS([self.num1,self.num2], "Test message")
        
        x = self.UTILS.getElements(DOM.Messages.thread_target_names, "Threads target names")
        bool_1_ok=False
        bool_2_ok=False
        for i in x:
            self.UTILS.logResult("info", "Thread: " + i.text)
            if i.text == self.Contact_1["name"]:
                bool_1_ok = True
            if i.text == self.Contact_2["name"]:
                bool_2_ok = True
                
        self.UTILS.TEST(bool_1_ok, "A thread exists for " +  self.Contact_1["name"])
        self.UTILS.TEST(bool_2_ok, "A thread exists for " + self.Contact_2["name"])