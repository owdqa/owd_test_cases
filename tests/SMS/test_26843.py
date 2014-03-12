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
from tests._mock_data.contacts import MockContact
#import time


class test_main(GaiaTestCase):
    
    test_msg = "Test message."
    
    _RESTART_DEVICE = True
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        
        #
        # Establish which phone number to use and set up the contacts.
        #
        self.nums = [self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"),
                        self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")]

        self.test_contacts = [MockContact(tel = {'type': 'Mobile', 
                                'value' : num}) for num in self.nums]        
        map(self.UTILS.insertContact, self.test_contacts)

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
        self.messages.createAndSendSMS(self.nums, "Test message")
        
        x = self.UTILS.getElements(DOM.Messages.thread_target_names, "Threads target names")

        # bools = [title in self.nums for title in x]

        f = lambda x : [elem["name"] for elem in x]
        bools = [title.text in f(self.test_contacts) for title in x]

        msgs = ["A thread exists for " + str(elem) for elem in f(self.test_contacts)]
        map(self.UTILS.TEST, bools, msgs)


        # bool_1_ok=False
        # bool_2_ok=False
        # for i in x:
        #     self.UTILS.logResult("info", "Thread: " + i.text)
        #     if i.text == self.Contact_1["name"]:
        #         bool_1_ok = True
        #     if i.text == self.Contact_2["name"]:
        #         bool_2_ok = True
                
        # self.UTILS.TEST(bool_1_ok, "A thread exists for " +  self.Contact_1["name"])
        # self.UTILS.TEST(bool_2_ok, "A thread exists for " + self.Contact_2["name"])