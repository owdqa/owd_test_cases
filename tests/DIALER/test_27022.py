# 27022:
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer
import time


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        self.dialer.launch()
        self.dialer.createMultipleCallLogEntries(self.phone_phone_numberber, 1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Open the call log and tap on the phone_numberber.
        #
        self.dialer.openCallLog()
        self.dialer.callLog_call(self.phone_number)

        # TODO: If we unblock this test to match v2.0, follow this code to complete it
        # elem = ("xpath", DOM.Dialer.call_log_number_xpath.format(self.phone_number))
        # entry = self.UTILS.element.getElement(elem,
        #                            "The call log for number {}".format(self.phone_number))
        # entry.tap()

        # TODO: Check that frame_calling_locator displays, wait 2 seconds, and hangUp
