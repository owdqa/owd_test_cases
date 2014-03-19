#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.email import Email
import time

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
        # Go into edit mode.
        #
        x= self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button" )
        x.tap()

        #
        # Get the last message.
        #
        x = self.UTILS.element.getElements(DOM.Messages.message_list, "Messages", False)[-1]

        #
        # Verify that the email address does not open the email app.
        #
        link = x.find_element("tag name", "a")
        link.tap()

        #
        # Now try to find the email app iframe.
        #
        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements( ("xpath", "//iframe[contains(@src,'email')]"),
                                       "Email app iframe")
