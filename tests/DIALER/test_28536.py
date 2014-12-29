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
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

        self.dialer = Dialer(self)

        # Get own number and incoming
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Calling to " + self.phone_number)
        self.incoming_number = self.UTILS.general.get_config_variable("incoming_call_number", "common")

        # Generate the incoming call
        self.marionette.switch_to_frame()
        self.data_layer.send_sms(self.incoming_number, "Call:" + self.phone_number)
        self.dialer.answer_and_hangup(2)

        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # Launch dialer app.
        self.dialer.launch()

        keypad_option = self.UTILS.element.getElement(DOM.Dialer.option_bar_keypad, "Keypad Option")
        keypad_option.tap()

        call_button = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call button")
        call_button.tap()

        # Make sure that after tapping, we get the last outgoing call in the call log
        phone_field = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = phone_field.get_attribute("value")

        self.UTILS.test.test(dialer_num == "", "Nothing in the input area")