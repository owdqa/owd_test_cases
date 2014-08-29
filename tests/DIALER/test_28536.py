# 28536: Press call button while call log only contains incoming and missed calls
# 
#  ** Prerrequisites
#         Call log only contains incoming and missed calls during all the test
#  ** Procedure
#         1. Open dialer app
#         2. Press call button
#
#  ** Expected result
#         Tapping on the Call button retrieves the most recent outgoing number from the call log

import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.dialer = Dialer(self)

        #
        # Get own number and incoming
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Calling to " + self.phone_number)
        self.incoming_number = self.UTILS.general.get_os_variable("GLOBAL_NUM_FOR_INCOMING_CALL")

        #
        # Generate the incoming call
        #
        self.marionette.switch_to_frame()
        self.data_layer.send_sms(self.incoming_number, "Call:" + self.phone_number)
        self.dialer.answer_and_hangup(2)

        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        # Launch dialer app.
        self.dialer.launch()

        x = self.UTILS.element.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call button")
        x.tap()

        # Make sure that after tapping, we get the last outgoing call in the call log
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        self.assertEqual(dialer_num, "", "Nothing in the input area")

        y = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screen shot of the result of tapping call button", y)
