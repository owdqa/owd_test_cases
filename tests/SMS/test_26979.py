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

        self.email_user = self.UTILS.general.get_os_variable("GMAIL_1_USER")
        self.email_address = self.UTILS.general.get_os_variable("GMAIL_1_EMAIL")
        self.email_pass = self.UTILS.general.get_os_variable("GMAIL_1_PASS")
 
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.general.get_os_variable("GMAIL_2_EMAIL")


    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Set up email account.
        #
        self.UTILS.network.getNetworkConnection()

        self.Email.launch()
        self.Email.setupAccount(self.email_user, self.email_address, self.email_pass)
 
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.phone_number], "Email {} one.".format(elf.emailAddy))
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Tap the email link.
        #
        link = x.find_element("tag name", "a")
        link.tap()

        z= self.UTILS.element.getElement(DOM.Messages.header_send_email_btn, "Edit button")
        z.tap()

        #
        # Switch to email frame and verify the email address is in the To field.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)
        x = self.UTILS.element.getElement(DOM.Email.compose_to_from_contacts, "To field")
        self.UTILS.test.TEST(x.text == self.emailAddy, 
                        "To field contains '{0}' (it was '{0}').".format(self.emailAddy))