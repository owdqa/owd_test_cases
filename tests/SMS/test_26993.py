#===============================================================================
# 26993: Tap on the header showing the name of a contact (contact's number with prefix)
#
# Pre-requisites:
# Have a contact whose phone number has a prefix.
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

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
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
        self.contacts = Contacts(self)
        self.Dialer = Dialer(self)

        phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        prefix = "0034"
        self.num1 = prefix + phone_number if not phone_number.startswith("+34") else prefix + phone_number[3:]
        self.num2 = phone_number[3:] if phone_number.startswith("+34") else phone_number

        self.contact = MockContact(tel={'type': 'Mobile', 'value': self.num1})

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
        # Create and send a new test message to this contact.
        #
        self.messages.startNewSMS()

        self.messages.selectAddContactButton()
        self.contacts.view_contact(self.contact["familyName"], False)
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.messages.checkIsInToField(self.contact["name"], True)

        self.messages.enterSMSMsg("Test message.")
        self.messages.sendSMS()

        x = self.messages.wait_for_received_msg_in_this_thread()

        #
        # Tap the header to call.
        #
        self.messages.header_call()

        #
        # Dialler is started with the number already filled in.
        #
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number")
        self.UTILS.test.test(self.num2 in x.get_attribute("value"),
                        "The phone number contains '{}' (it was '{}').".format(self.num1, x.get_attribute("value")))
