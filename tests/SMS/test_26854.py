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
    
    _RESTART_DEVICE = True
    
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

        #
        # Remember the 'real' current date and time.
        #
        self.NOW_EPOCH =time.time()
        _now           = self.UTILS.getDateTimeFromEpochSecs(self.NOW_EPOCH)

        #
        #=============================================================================
        #
        self.UTILS.logResult("info", "<b><u>Reading an sms from 2 months ago ...</u></b>")
        _test_month = _now.tm_mon - 2
        x = self.UTILS.setTimeToSpecific(p_month=_test_month)
        expected_str = "%s/%s/%s" % (str(x.tm_mon).zfill(2), str(x.tm_mday).zfill(2), x.tm_year)
          
        self._sendSMS("2 months ago")         
        self._checkTimeStamp(expected_str)
  
 
        #
        #=============================================================================
        #
        self.UTILS.logResult("info", "<b><u>Reading an sms from 7 days ago ...</u></b>")
        _test_day = _now.tm_mday - 7   
        x = self.UTILS.setTimeToSpecific(p_day=_test_day)
            
        self._sendSMS("7 days ago")
          
        expected_str = "%s/%s/%s" % (str(x.tm_mon).zfill(2), str(x.tm_mday).zfill(2), x.tm_year)
        self._checkTimeStamp(expected_str)
          

        #
        #=============================================================================
        #
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(6,1,-1):
  
            _test_day = _now.tm_mday - i     
            x = self.UTILS.setTimeToSpecific(p_day=_test_day)
                
            _dayname = days[x.tm_wday]
            self.UTILS.logResult("info", "<b><u>Reading an sms from %s days ago (%s) ...</u></b>" % (str(i), _dayname))
              
            self._sendSMS("DAY: %s" % _dayname)
            self._checkTimeStamp(_dayname)
              
              
        #
        #=============================================================================
        #
        self.UTILS.logResult("info", "<b><u>Reading an sms from yesterday ...</u></b>")
        _test_day = _now.tm_mday - 1   
        x = self.UTILS.setTimeToSpecific(p_day=_test_day)         
        self._sendSMS("DAY: YESTERDAY")
        self._checkTimeStamp("YESTERDAY")
    
    
        #
        #=============================================================================
        #
        self.UTILS.logResult("info", "<b><u>Reading an sms from today ...</u></b>")
        self.data_layer.set_time( self.NOW_EPOCH * 1000)
 
        self._sendSMS("DAY: TODAY")
        self._checkTimeStamp("TODAY")
        
        
    def _sendSMS(self, p_str):
        #
        # Sends an sms.
        #
        self.messages.launch()
        self.messages.createAndSendSMS([self.num], p_str)
        self.messages.waitForReceivedMsgInThisThread()
        self.apps.kill_all()
        
    def _checkTimeStamp(self, p_str):
        #
        # Sets the device time back to 'now', opens the sms / thread and
        # checks that the expected timestamp header is present.
        #
        # This is slow, but I can't find a way to see headers that are off the top
        # of the screen, so I ended up doing it this way.
        #
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "(Screenshot and html dump at this point ...)", x)
        self.UTILS.setTimeToNow()

        self.messages.launch()
        self.messages.openThread(self.num)
        x = self.UTILS.getElements(DOM.Messages.message_timestamps, "Message timestamp headers", False)[-1]
        self.UTILS.TEST(p_str.lower() in x.text.lower(), 
                        "<b>Last message timestamp header contains <u>'%s'</u> (it was '%s').</b>" % \
                        (p_str, x.text))

       