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

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.messages   = Messages(self)
        
        self.num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        return
        self.UTILS.TEST(False, "ROY RESTART DEVICE - I am still developing this so please ignore me!!")
        
        x=time.time()
        _now = self.UTILS.getDateTimeFromEpochSecs(x)
        
        #
        # Send a message from today.
        #
        self.messages.launch()
        self.messages.createAndSendSMS([self.num], "Today")
        self.apps.kill_all()
        time.sleep(5)
        
        #
        # Send a message from yesterday.
        #
        _yesterday = _now.tm_mday - 1
        self.UTILS.setTimeToSpecific(p_day=_yesterday)
        self.messages.launch()
        self.messages.createAndSendSMS([self.num], "Yesterday")
        self.apps.kill_all()
        time.sleep(5)
        
        #
        # Send a message from each day from the day before yesterday until a week ago.
        #
        for i in range(2, 6):
            _test_day = _now.tm_mday - i
            self.UTILS.setTimeToSpecific(p_day=_test_day)
            self.messages.launch()
            self.messages.createAndSendSMS([self.num], "Today %s, this was sent on day: %s" % (_now.tm_mday,_test_day))
            self.apps.kill_all()
            time.sleep(5)

        #
        # Send a message from two months ago.
        #
        _test_month = _now.tm_mon - 2
        self.UTILS.setTimeToSpecific(p_month=_test_month)
        self.messages.launch()
        self.messages.createAndSendSMS([self.num], "2 months ago")
        self.apps.kill_all()
        time.sleep(5)
        
        return
        

        
        #
        # Get the time of this thread (just hour and AM in case it took longer than
        # 1 minute to send the message).
        #
        _HH = self.messages.timeOfThread(self.num)[:2]
        _AM = self.messages.timeOfThread(self.num)[-2:]
        self.UTILS.TEST(_HH == "10", "Thread hour is 10 (it was " + _HH + ").", False)
        self.UTILS.TEST(_AM == "AM", "Thread timestamp says <b>AM</b> (it was " + _AM + ").", False)
        
        #
        # Kill the sms app (just makes my life easier!).
        #
        self.apps.kill_all()

        #
        # Change the time to afternoon.
        #
        self.UTILS.setTimeToSpecific(14,0)
        
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

