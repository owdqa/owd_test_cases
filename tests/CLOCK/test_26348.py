#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.clock import Clock
from OWDTestToolkit.apps.settings import Settings
import datetime
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.clock = Clock(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Set the volume to be low (no need to wake up the office! ;o)
        #
        self.settings.setAlarmVolume(0)

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
        # Create an alarm that is 1 minute in the future.
        #
        # (Make sure we're not about to do this at the end of a minute or an hour.)
        #
        now_mins = time.strftime("%M", time.gmtime())
        diff_m = 60 - int(now_mins)
        if diff_m <= 1:
            time.sleep(60)

        now_secs = time.strftime("%S", time.gmtime())
        diff_s = 60 - int(now_secs)
        if diff_s <= 15:
            time.sleep(diff_s)

        t = datetime.datetime.now() + datetime.timedelta(minutes=1)

        title = "Test alarm"
        self.clock.createAlarm(t.hour, t.minute, title)

        #
        # Return to the main screen (since this is where the user will
        # most likely be when the alarm goes off).
        #
        self.UTILS.home.goHome()

        #
        # Check the statusbar icon exists.
        #
        self.UTILS.test.TEST(self.clock.checkStatusbarIcon(), "Alarm icon is present in statusbar.")

        #
        # Wait for the alarm to start.
        #
        self.clock.checkAlarmRingDetails(t.hour, t.minute, title)
