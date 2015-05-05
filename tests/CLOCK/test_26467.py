from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.clock import Clock
import time


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.clock = Clock(self)
        self.data_layer.set_setting("time.timezone", "Europe/Madrid")
        self.data_layer.set_setting("time.timezone.user-selected", "Europe/Madrid")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch clock app.
        self.apps.kill_all()
        time.sleep(3)
        self.clock.launch()

        # Check that the face is analog.
        x = self.UTILS.element.getElement(DOM.Clock.analog_face, "Analog clock face")

        # Tap the clock face.
        self.UTILS.reporting.logResult("info", "Tapping the clock face ...")
        try:
            x.tap()
            self.wait_for_element_displayed(*DOM.Clock.digital_face)
        except:

            # For some reason this randomly doesn't work, so try again.
            self.UTILS.reporting.logResult("info",
                                 "<b>Note:</b> failed to tap the analog face - " +
                                 "suspect this is just a Marionette issue so I'm trying again.")
            self.apps.kill_all()
            time.sleep(2)
            self.clock.launch()
            x = self.UTILS.element.getElement(DOM.Clock.analog_face, "Analog clock face")
            x.tap()

        # Check this is now the digital clock face.
        self.UTILS.element.waitForElements(DOM.Clock.digital_face, "Digital clock face")

        # Verify the time is correct (digits for hh and mm need to be padded).
        device_ampm = self.UTILS.element.getElement(("xpath", "//*[@id='clock-hour24-state']"), "Clock time am / pm").text
        device_hhmm = self.UTILS.element.getElement(("xpath", "//*[@id='clock-time']"), "Clock time hh:mm").text
        device_hh = device_hhmm.split(":")[0].zfill(2)
        device_mm = device_hhmm.split(":")[1].zfill(2)

        device_time = device_hh + ":" + device_mm + device_ampm.zfill(2)

        now_hhmm = time.strftime("%I:%M")
        now_ampm = time.strftime("%r")[-2:]
        now_time = now_hhmm + now_ampm

        self.UTILS.test.test(now_time == device_time,
                        "Digital display time is correct (now = '" + now_time + "', display = '" + device_time + "').",
                        False)

        # Tap the clock face.
        x = self.UTILS.element.getElement(DOM.Clock.digital_face, "Digital clock face", False)
        self.UTILS.reporting.logResult("info", "Tapping the clock face ...")
        try:
            x.tap()
            self.wait_for_element_displayed(*DOM.Clock.analog_face)
        except:

            # For some reason this randomly doesn't work, so try again.
            self.UTILS.reporting.logResult("info",
                                 "<b>Note:</b> failed to tap the digital face - " +
                                 "suspect this is just a Marionette issue so I'm trying again.")
            self.UTILS.iframe.switchToFrame(*DOM.Clock.frame_locator)
            x = self.UTILS.element.getElement(DOM.Clock.digital_face, "Digital clock face")
            x.tap()

        # Check that the face is analog again.
        self.UTILS.element.waitForElements(DOM.Clock.analog_face, "Analog clock face")
