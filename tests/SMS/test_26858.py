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
        
        self.num1 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.num2 = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM_SHORT")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Set time on device to morning.
        #
        self.UTILS.setTimeToSpecific(p_hour=10,p_minute=0)
        
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
        self.messages.createAndSendSMS([self.num1], self._TestMsg)
        
        #
        # Return to the threads screen and check the time of this thread.
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        time.sleep(1)
        
        #
        # Get the time of this thread (just hour and AM in case it took longer than
        # 1 minute to send the message).
        #
        _HH = self.messages.timeOfThread(self.num1)[:2]
        _AM = self.messages.timeOfThread(self.num1)[-2:]
        self.UTILS.TEST(_HH == "10", "Thread hour is 10 (it was " + _HH + ").", False)
        self.UTILS.TEST(_AM == "AM", "Thread timestamp says <b>AM</b> (it was " + _AM + ").", False)
        
        #
        # Kill the sms app (just makes my life easier!).
        #
        self.apps.kill_all()

        #
        # Change the time to afternoon.
        #
        self.UTILS.setTimeToSpecific(p_hour=14,p_minute=0)
        
        #
        # Send a message from num2.
        #
        self.messages.launch()
        self.messages.createAndSendSMS([self.num2], self._TestMsg)
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        time.sleep(1)

        #
        # Get the time of this thread (just hour and AM in case it took longer than
        # 1 minute to send the message).
        #
        _HH = self.messages.timeOfThread(self.num2)[:1]
        _PM = self.messages.timeOfThread(self.num2)[-2:]
        self.UTILS.TEST(_HH == "2", "Thread hour is 2 (it was " + _HH + ").", False)
        self.UTILS.TEST(_PM == "PM", "Thread timestamp says <b>PM</b> (it was " + _PM + ").", False)

