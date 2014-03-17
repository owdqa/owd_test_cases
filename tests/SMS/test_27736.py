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
from OWDTestToolkit.apps.contacts import Contacts

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)
        
        #
        # Establish which phone number to use.
        #
        self.telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Using target telephone number " + self.telNum)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        self.messages.launch()
        
        self.messages.createAndSendSMS( [self.telNum], 
                                        "Just creating a message thread.")
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        
        #
        # Return to main SMS page.
        #
        self.messages.closeThread()
        
        #
        # Press the edit button (without selecting any threads).
        #
        self.messages.editAndSelectThreads([])
        
        #
        # Check that the delete button is not enabled.
        #
        x = self.UTILS.getElement(DOM.Messages.delete_threads_button, "Delete button")
        self.UTILS.TEST(x.get_attribute("class") == "disabled", "Delete button is not enabled.")
