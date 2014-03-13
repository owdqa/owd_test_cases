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
    
    _TestMsg     = "Test message."
    
    _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        #
        # Establish which phone number to use.
        #
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num2 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Make sure we have no contacts.
        #
        self.data_layer.remove_all_contacts()
        
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
            if i.text == self.num1:
                bool_1_ok = True
            if i.text == self.num2:
                bool_2_ok = True
                
        self.UTILS.TEST(bool_1_ok, "A thread exists for " + str(self.num1))
        self.UTILS.TEST(bool_2_ok, "A thread exists for " + str(self.num2))
        
        
        
        