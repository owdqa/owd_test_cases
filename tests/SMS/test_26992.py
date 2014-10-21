#===============================================================================
# 26992: Tap on the header showing the name of a contact (contact's number
# without prefix)
#
# Pre-requisites:
# Have a contact whose phone number has no prefix.
# Send/receive at least one SMS to have a thread
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
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact
from OWDTestToolkit.apps.dialer import Dialer


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.Dialer = Dialer(self)

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        self.contact = MockContact(tel={'type': 'Mobile', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.startNewSMS()

        self.messages.selectAddContactButton()
        self.contacts.view_contact(self.contact["familyName"], False)
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.checkIsInToField(self.contact["name"], True)

        self.messages.enterSMSMsg("Test message.")
        self.messages.sendSMS()
        send_time = self.messages.last_sent_message_timestamp()

        self.messages.waitForReceivedMsgInThisThread(send_time=send_time)

        #
        # Tap the header to call.
        #
        self.messages.header_call()

        #
        # Dialer is started with the number already filled in.
        #
        time.sleep(2)
        phone_field = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = phone_field.get_attribute("value")

        self.UTILS.test.TEST(self.phone_number == dialer_num,
                        "The phone is '{}' (expected '{}').".\
                        format(dialer_num, self.phone_number))
