# 26835: Make a call by selecting an entry in the log (airplane mode enabled)
# ** Procedure
#       1- Open Settings app
#       2- Enabled airplane mode
#       ER1
#       3- Open Call log
#       4- Press over an entry
#       ER2
#       5- Pres OK
#       ER3
# ** Expected Result
#       ER1 Airplane mode is enabled
#       ER2 A confirmation dialog should be shown to the user stating "In order to make a call, you must first
#       disable flight mode" and an "OK" button.
#       ER3 When the "OK" button is pressed, the dialogue is closed and the user is returned to the call log.
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer

import sys
sys.path.insert(1, "./")
from tests.i18nsetup import setup_translations


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        _ = setup_translations(self)

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        # Fill the call log with some entries
        self.dialer.launch()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 1)
        self.data_layer.set_setting("airplaneMode.enabled", True)
        self.wait_for_condition(lambda m: self.data_layer.get_setting("airplaneMode.enabled"),
                                timeout=30, message="No airplane mode enabled")

    def tearDown(self):
        self.data_layer.set_setting("airplaneMode.enabled", False)
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.openCallLog()

        elem = ("xpath", DOM.Dialer.call_log_number_xpath.format(self.phone_number))
        entry = self.UTILS.element.getElement(elem, "The call log for number {}".format(self.phone_number))
        entry.tap()

        warning_header = (DOM.GLOBAL.confirmation_msg_header[0],
                            DOM.GLOBAL.confirmation_msg_header[1].format(_("Airplane mode activated")))

        _content = _("To make a call you need to disable airplane mode in settings.")
        warning_content = (DOM.GLOBAL.confirmation_msg_content[0],
                            DOM.GLOBAL.confirmation_msg_content[1].format(_content))

        self.UTILS.element.getElement(warning_header, "Airplane mode warning [header]")
        self.UTILS.element.getElement(warning_content, "Airplane mode warning [content]")
    
        ok_btn = self.UTILS.element.getElement(DOM.GLOBAL.confirmation_msg_ok_btn, "OK button")
        ok_btn.tap()

        self.UTILS.element.waitForElements(DOM.Dialer.call_log_filter, "Call log filter")
