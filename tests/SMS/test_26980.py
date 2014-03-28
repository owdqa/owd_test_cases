#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.email import Email
from tests._mock_data.contacts import MockContact
#import time


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.Email = Email(self)

        self.USER1 = self.UTILS.general.get_os_variable("GMAIL_1_USER")
        self.EMAIL1 = self.UTILS.general.get_os_variable("GMAIL_1_EMAIL")
        self.PASS1 = self.UTILS.general.get_os_variable("GMAIL_1_PASS")
 
        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.general.get_os_variable("GMAIL_2_EMAIL")

        self.contact = MockContact(email = {'type': 'Personal', 'value': self.emailAddy})

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Set up email account.
        #
        self.UTILS.network.getNetworkConnection()

        self.Email.launch()
        self.Email.setupAccount(self.USER1, self.EMAIL1, self.PASS1)
 
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], "Email {} one.".format(self.emailAddy))
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Tap the email link.
        #
        link = x.find_element("tag name", "a")
        link.tap()

        #
        # Press 'add to existing contact' button.
        #
        w = self.UTILS.element.getElement(DOM.Messages.header_send_email_btn, "Send email button")
        w.tap()

        #
        # Switch to email frame and verify the email address is in the To field.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
        x = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "To field")
        self.UTILS.test.TEST(x.text == self.emailAddy, 
                        "To field contains '{}' (it was '{}').".format(self.emailAddy, self.emailAddy))