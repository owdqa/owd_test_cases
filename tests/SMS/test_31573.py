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
from OWDTestToolkit.apps.messages import Messages
from marionette import Actions

class test_main(GaiaTestCase):
    #
    # Restart device to start without sms
    #
    _RESTART_DEVICE = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.actions = Actions(self.marionette)

        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.logComment("Sending sms to telephone number " + self.target_telNum)
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Sometimes causes a problem if not cleared.
        #
        self.UTILS.clearAllStatusBarNotifs()

        #
        # Create message - 5 x 10 chars.
        #
        sms_message = "0123456789" * 5
        self.UTILS.logComment("Message length sent: {}".format((len(sms_message))))
        
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], sms_message)
        
        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)

        self.messages.fordwardMessage("sms", self.target_telNum)
