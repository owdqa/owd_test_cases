import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.calendar import Calendar



class test_main(GaiaTestCase):

    offset_days = 1

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.calendar = Calendar(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.date_and_time.setTimeToNow()

        # Launch contacts app.
        self.calendar.launch()

        _today = self.UTILS.date_and_time.getDateTimeFromEpochSecs(int(time.time()))

        #===================================================================================================

        # MONTH view
        self.calendar.setView("month")

        self.UTILS.reporting.logResult("info", "<b>Testing <u>month</u> view for <i>today</i> ...</b>")
        self.calendar.setView("today")
        self.monthViewTests(_today, True)

        self.UTILS.reporting.logResult("info", "<b>Testing <u>month</u> view for <i>{} days ago</i> ...</b>"
                             .format(self.offset_days))
        x = self.calendar.changeDay(self.offset_days, "month")
        self.monthViewTests(x, False)

        #===================================================================================================

        # WEEK view
        self.calendar.setView("week")

        self.UTILS.reporting.logResult("info", "<b>Testing <i>week</i> view for <i>today</i> ...</b>")
        self.calendar.setView("today")
        self.weekViewTests(_today)

        self.UTILS.reporting.logResult("info", "<b>Testing <u>week</u> view for <i>{} days ago</i> ...</b>"
                             .format(self.offset_days))
        x = self.calendar.changeDay(self.offset_days, "week")
        self.weekViewTests(x)

        #===================================================================================================

        # DAY view
        self.calendar.setView("day")

        self.UTILS.reporting.logResult("info", "<b>Testing <i>day</i> view for <i>today</i> ...</b>")
        self.calendar.setView("today")
        self.dayViewTests(_today)

        self.UTILS.reporting.logResult("info", "<b>Testing <u>day</u> view for <i>{} days ago</i> ...</b>"
                             .format(self.offset_days))
        x = self.calendar.changeDay(self.offset_days, "day")
        self.dayViewTests(x)

    def dayViewTests(self, now):
        x = self.UTILS.element.getElement(DOM.Calendar.current_view_header, "Day view header")

        self.UTILS.test.test(now.day_name.lower() in x.text.lower(),
                        "'{}' is in the header ('{}').".format(now.day_name, x.text))

        self.UTILS.test.test(now.month_name[:3].lower() in x.text.lower(),
                        "'{}' is in the header ('{}').".format(now.month_name[:3], x.text))

        self.UTILS.test.test(str(now.mday) in x.text,
                        "'{}' is in the header ('{}').".format(now.mday, x.text))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot in day view with 'today' selected:", x)

    def weekViewTests(self, now):
        # Loop through displayed days, building the report string + checking our day is there...
        x = self.UTILS.element.getElements(DOM.Calendar.wview_active_days, "Active days")
        testStr = "{} {}".format(now.day_name[:3].upper(), now.mday)
        x_str = ""

        boolOK = False
        for i in range(len(x)):
            if x_str != "":
                x_str = x_str + ", "
            x_str = x_str + x[i].text
            if testStr in x[i].text:
                boolOK = True

        self.UTILS.test.test(boolOK, "Selected day ('{}') is one of the displayed days: '{}'".format(testStr, x_str))

        x = self.UTILS.element.getElement(DOM.Calendar.current_view_header, "Week view header")
        self.UTILS.test.test(now.month_name.lower() in x.text.lower(),
                        "'{}' is in the header ('{}').".format(now.month_name, x.text))

        self.UTILS.test.test(str(now.year) in x.text,
                        "'{}' is in the header ('{}').".format(now.year, x.text))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot in week view with 'today' selected:", x)

    def monthViewTests(self, now, today):
        # Highlighted cell is correct ...
        el_id_str = "d-{}-{}-{}".format(now.year, now.mon - 1, now.mday)
        self.UTILS.element.waitForElements(("xpath",
                                    "//li[@data-date='{}' and contains(@class, 'selected')]".format(el_id_str)),
                                  "Selected day for {}/{}/{}".format(now.mday, now.mon, now.year), True, 2, False)

        # Selected day string is correct ...
        if today:
            x = self.UTILS.element.getElement(DOM.Calendar.mview_selected_day_title, "Selected day detail string")
            _expected_str = "{}".format(now.mday)
            self.UTILS.test.test(_expected_str.lower() in x.text.lower(),
                            "Day detail string: '{}' contains today's details ('{}').".format(x.text, _expected_str))
        else:
            x = self.UTILS.element.getElement(DOM.Calendar.mview_selected_day_title_future, "Selected day detail string")

        x = self.UTILS.element.getElement(DOM.Calendar.current_view_header, "Month view header")
        self.UTILS.test.test(now.month_name.lower() in x.text.lower(),
                        "'{}' is in the header ('{}').".format(now.month_name, x.text))

        self.UTILS.test.test(str(now.year) in x.text,
                        "'{}' is in the header ('{}').".format(now.year, x.text))
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot in month view with 'today' selected:", x)
