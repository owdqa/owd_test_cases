from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time


class test_main(SpreadtrumTestCase):

    _now = ""

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.num = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.date_and_time.set_time_to_now()
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.statusbar.clearAllStatusBarNotifs()
        """
        Launch messages app & delete all Threads
        Make sure we have no threads
        """

        self.messages.launch()

        # Remember the 'real' current date and time.
        one_day = 86400
        self.NOW_EPOCH = time.time()
        self._now = self.UTILS.date_and_time.getDateTimeFromEpochSecs(self.NOW_EPOCH)

        #=============================================================================
        self.UTILS.reporting.logResult("info", " ")
        self.UTILS.reporting.logResult("info", "--------------------------")
        self.UTILS.reporting.logResult("info", "<b><u>Reading an sms from 2 months ago...</u></b>")

        t = self.UTILS.date_and_time.getDateTimeFromEpochSecs(self.NOW_EPOCH - (64 * one_day))
        self.UTILS.date_and_time.setTimeToSpecific(p_year=t.year, p_month=t.mon, p_day=t.mday)

        expected_str = "{}/{}/{}".format(str(t.mon).zfill(2), str(t.mday).zfill(2), t.year)

        self.data_layer.send_sms(self.num, "2 months ago")
        self.UTILS.statusbar.wait_for_notification_toaster_detail("2 months ago", timeout=120)
        self._checkTimeStamp(expected_str)

        #=============================================================================
        self.UTILS.reporting.logResult("info", " ")
        self.UTILS.reporting.logResult("info", "--------------------------")
        self.UTILS.reporting.logResult("info", "<b><u>Reading an sms from 6 days ago...</u></b>")

        t = self.UTILS.date_and_time.getDateTimeFromEpochSecs(self.NOW_EPOCH - (6 * one_day))
        x = self.UTILS.date_and_time.setTimeToSpecific(p_year=t.year, p_month=t.mon, p_day=t.mday)

        expected_str = "{}/{}/{}".format(str(t.mon).zfill(2), str(t.mday).zfill(2), t.year)

        self.data_layer.send_sms(self.num, "6 days ago")
        self.UTILS.statusbar.wait_for_notification_toaster_detail("6 days ago", timeout=120)
        self._checkTimeStamp(expected_str)

        #=============================================================================
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i in range(5, 1, -1):
            self.UTILS.reporting.logResult("info", " ")
            self.UTILS.reporting.logResult("info", "--------------------------")
            t = self.UTILS.date_and_time.getDateTimeFromEpochSecs(self.NOW_EPOCH - (i * one_day))
            x = self.UTILS.date_and_time.setTimeToSpecific(p_year=t.year, p_month=t.mon, p_day=t.mday)

            _dayname = days[x.tm_wday]
            self.UTILS.reporting.logResult("info", "<b><u>Reading an sms from {} days ago ({})...</u></b>".\
                                           format(i, _dayname))

            text = "DAY: {} ({} days ago).".format(_dayname, str(i))
            self.data_layer.send_sms(self.num, text)
            self.UTILS.statusbar.wait_for_notification_toaster_detail(text, timeout=120)
            self._checkTimeStamp(_dayname.upper())

        #=============================================================================
        self.UTILS.reporting.logResult("info", " ")
        self.UTILS.reporting.logResult("info", "--------------------------")
        self.UTILS.reporting.logResult("info", "<b><u>Reading an sms from yesterday...</u></b>")
        t = self.UTILS.date_and_time.getDateTimeFromEpochSecs(self.NOW_EPOCH - (1 * one_day))
        x = self.UTILS.date_and_time.setTimeToSpecific(p_year=t.year, p_month=t.mon, p_day=t.mday)
        self.data_layer.send_sms(self.num, "DAY: YESTERDAY")
        self.UTILS.statusbar.wait_for_notification_toaster_detail("DAY: YESTERDAY", timeout=120)
        self._checkTimeStamp("YESTERDAY")

        #=============================================================================
        self.UTILS.reporting.logResult("info", " ")
        self.UTILS.reporting.logResult("info", "--------------------------")
        self.UTILS.reporting.logResult("info", "<b><u>Reading an sms from today ...</u></b>")
        self.data_layer.set_time(self.NOW_EPOCH * 1000)

        self.data_layer.send_sms(self.num, "DAY: TODAY")
        self.UTILS.statusbar.wait_for_notification_toaster_detail("DAY: TODAY", timeout=120)
        self._checkTimeStamp("TODAY")

    def _checkTimeStamp(self, p_str):
        """
        Sets the device time back to 'now', opens the sms / thread and
        checks that the expected timestamp header is present.
        """

        # This is slow, but I can't find a way to see headers that are off the top
        # of the screen, so I ended up doing it this way.
        #
        self.UTILS.reporting.logResult("info", "Setting device time back to the 'real' date and time.")
        self.data_layer.set_time(self.NOW_EPOCH * 1000)

        self.UTILS.date_and_time.waitForDeviceTimeToBe(p_year=self._now.year,
                                         p_month=self._now.mon,
                                         p_day=self._now.mday,
                                         p_hour=self._now.hour,
                                         p_minute=self._now.min)

        self.messages.launch()
        self.messages.openThread(self.num)
        time.sleep(2)
        x = self.UTILS.element.getElements(DOM.Messages.message_timestamps, "Message date header", False)[-1]
        self.UTILS.test.test(p_str == x.text.encode("utf8"),
                        "<b>Last message timestamp header is <u>'{}'</u> </b>(expected <b>'{}'</b>).".\
                        format(x.text, p_str), stop_on_error=True)
        time.sleep(3)
        self.messages.closeThread()
