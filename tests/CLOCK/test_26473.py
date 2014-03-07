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
#from datetime 
import datetime, time   

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.clock      = Clock(self)
        self.settings   = Settings(self)
                
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):    
        #
        # Launch clock app.
        #
        self.clock.launch()
        
        #
        # Delete all previous alarms.
        #
        #
        self.clock.deleteAllAlarms() 

        #
        # Create an alarm that is 2 minutes in the future.
        #
        # (Make sure we're not about to do this at the end of a minute or an hour.)
        #
        now_mins = time.strftime("%M", time.gmtime())
        diff_m   = 60 - int(now_mins)
        if diff_m <= 1:
            time.sleep(60)
        
        now_secs = time.strftime("%S", time.gmtime())
        diff_s   = 60 - int(now_secs)
        if diff_s <= 15:
            time.sleep(diff_s)


        t = datetime.datetime.now() + datetime.timedelta(minutes=2)
        
        _hour   = t.hour
        _minute = t.minute
        _title  = "Test alarm"

        self.clock.createAlarm(_hour, _minute, _title)
        
        #
        # Restart the Clock app.
        #
        self.clock.launch()
        
        #
        # Delete the alarm.
        #
        self.clock.deleteAllAlarms()