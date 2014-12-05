# 26834: Make a call by entering manually the phone number and clicking the
# "dial button" afterwards (airplane mode enabled)
# ** Procedure
#       1- Open Settings app
#       2- Enabled ariplane mode
#       ER1
#       3- Open Dialer
#       4- Entering manually the phone number and click the "dial button"
#       ER2
#       5- Pres OK
#       ER3
#
# ** Expected Results
#
#       ER1 Airplane mode is enabled
#       ER2 A confirmation dialog should be shown to the user stating "In order to make a call,
#       you must first disable flight mode" and an "OK" button.
#       ER3 When the "OK" button is pressed, the dialogue is closed and the user
#       is returned to the dialpad with the number to be called shown in the
#       dialpad.

import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer
from tests.i18nsetup import setup_translations


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        _ = setup_translations(self)
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

    def tearDown(self):
        self.data_layer.set_setting("airplaneMode.enabled", False)
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.set_setting("airplaneMode.enabled", True)
        self.wait_for_condition(lambda m: self.data_layer.get_setting("airplaneMode.enabled"),
                                timeout=30, message="No airplane mode enabled")
        self.dialer.launch()
        self.dialer.enterNumber(self.phone_number)
        call_button = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call number button")
        call_button.tap()

        warning_header = (DOM.GLOBAL.confirmation_msg_header[0],
                          DOM.GLOBAL.confirmation_msg_header[1].format(_("Airplane mode activated")))

        _content = _("To make a call you need to disable airplane mode in settings.")
        warning_content = (DOM.GLOBAL.confirmation_msg_content[0],
                           DOM.GLOBAL.confirmation_msg_content[1].format(_content))

        self.UTILS.element.getElement(warning_header, "Airplane mode warning [header]")
        self.UTILS.element.getElement(warning_content, "Airplane mode warning [content]")

        ok_btn = self.UTILS.element.getElement(DOM.GLOBAL.confirmation_msg_ok_btn, "OK button")
        ok_btn.tap()

        phone_field = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_number = phone_field.get_attribute("value")
        self.UTILS.test.test(str(self.phone_number) in dialer_number,
                             "After cancelling, phone number field still contains '{}'".format(self.phone_number))
