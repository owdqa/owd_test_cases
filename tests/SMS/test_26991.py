#===============================================================================
# 26991: Tap on the header showing the name of a contact
#
# Pre-requisites:
# Receive/send an SMS from a number which is already stored on the Address book
# as a contact.
# Contact saved manually
#
# Procedure:
# 1. Open the SMS thread
# 2. On the thread view tap on the header where the contact's name is shown (ER1)
# 3. Press green key (ER2)
#
# Expected results:
# ER1. The dialer is open with the contact's number pre-filled in.
# ER2. The call is initiated
#===============================================================================
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.apps.dialer import Dialer


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Dialer = Dialer(self)

        self.phone_number = self.UTILS.general.get_config_variable("GLOBAL_TARGET_SMS_NUM")
        self.test_msg = "Test message at {}".format(time.time())

        self.contact = MockContact(tel={'type': 'Mobile', 'value': self.phone_number})
        self.UTILS.general.insertContact(self.contact)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Create and send a new test message.
        #
        self.data_layer.send_sms(self.phone_number, self.test_msg)
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        self.UTILS.statusbar.click_on_notification_detail(self.test_msg, DOM.Messages.frame_locator)

        #
        # Tap the header to call.
        #
        self.messages.header_call()

        #
        # Dialer is started with the number already filled in.
        #
        current = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number").get_attribute("value")
        self.UTILS.test.test(self.phone_number == current,
                        "The phone number contains '{}' (expected '{}').".format(current, self.phone_number))

        #
        # Dial the number.
        #
        self.Dialer.call_this_number_and_hangup(5)
