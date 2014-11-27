import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)

        #
        # Get own number and incoming
        #
        self.phone_number = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.call_number = self.UTILS.general.get_config_variable("TARGET_CALL_NUMBER")
        self.incoming_number = self.UTILS.general.get_config_variable("GLOBAL_NUM_FOR_INCOMING_CALL")
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # Launch dialer app.
        self.dialer.launch()

        self.dialer.enterNumber(self.call_number)
        self.dialer.call_this_number_and_hangup(2)

        time.sleep(2)
        self.UTILS.messages.create_incoming_sms(self.incoming_number, "Call:" + self.phone_number)
        self.UTILS.iframe.switch_to_frame(*DOM.Dialer.frame_locator)
        self.dialer.answer_and_hangup(3)

        time.sleep(2)
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)
        time.sleep(2)
        self.dialer.enterNumber(self.call_number)
        self.dialer.call_this_number()

        self.UTILS.messages.create_incoming_sms(self.incoming_number, "Call:" + self.phone_number)
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.wait_for_element_displayed('id', 'incoming-answer', timeout=50)
        answer = self.marionette.find_element('id', 'incoming-answer')
        if answer:
            answer.tap()
        time.sleep(2)
        self.dialer.hangUp()
        time.sleep(5)
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.dialer.hangUp()
