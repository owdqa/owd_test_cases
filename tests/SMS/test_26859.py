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
import time

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
        self.settings   = Settings(self)
        
        
        self.target_telNum = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()
        
        #
        # Make sure we have no threads (currently blocked - use _RESTART_DEVICE instead).
        #
#         self.messages.deleteAllThreads()
        
        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.target_telNum], self._TestMsg)
        
        #
        # Check the time of this message.
        #
        _ORIG_MSG_TIMESTAMP = self.messages.timeOfLastMessageInThread()
        self.UTILS.logResult("info", "(original message timestamp = '" + _ORIG_MSG_TIMESTAMP + "'.)")
        
        #
        # Return to the threads screen and check the time of this thread.
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        time.sleep(1)
        
        #
        # Get the time of this thread.
        #
        _ORIG_THREAD_TIMESTAMP = self.messages.timeOfThread(self.target_telNum)
        self.UTILS.logResult("info", "(original thread timestamp = '" + _ORIG_THREAD_TIMESTAMP + "'.)")
        
        #
        # Change to a (unlikely!) timezone.
        #
        self.apps.kill_all()
        self.UTILS.setTimeToNow("Antarctica", "Casey")

        #
        # Open the sms app again.
        #
        self.messages.launch()
        
        #
        # Get the new thread time.
        #
        _NEW_THREAD_TIMESTAMP = self.messages.timeOfThread(self.target_telNum)
        self.UTILS.logResult("info", "(new thread timestamp = '" + _NEW_THREAD_TIMESTAMP + "'.)")
        
        #
        # Open our thread.
        #
        self.messages.openThread(self.target_telNum)
        
        #
        # Get the new message time.
        #
        _NEW_MSG_TIMESTAMP = self.messages.timeOfLastMessageInThread()
        self.UTILS.logResult("info", "(new message timestamp = '" + _NEW_MSG_TIMESTAMP + "'.)")
        
        self.UTILS.TEST(_ORIG_THREAD_TIMESTAMP != _NEW_THREAD_TIMESTAMP, "Thread timestamp has changed.")
        self.UTILS.TEST(_ORIG_MSG_TIMESTAMP    != _NEW_MSG_TIMESTAMP   , "Message timestamp has changed.")
