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
from OWDTestToolkit.apps.contacts import Contacts
from marionette import Actions


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

        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.emailAddy = self.UTILS.general.get_os_variable("GMAIL_1_EMAIL")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], "Hello " + self.emailAddy + " old bean.")
        x = self.messages.waitForReceivedMsgInThisThread()

        self.UTILS.element.waitForNotElements(DOM.Messages.edit_mode_wrapper,
                                        "Main wrapper in edit mode")

        #
        # Tap on edit mode.
        #
        y = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        y.tap()

        #
        # Verify that the edit wrapper is now displayed.
        #
        self.UTILS.element.waitForElements(DOM.Messages.edit_mode_wrapper, "Main wrapper in edit mode")

        #
        # Long press the email link.
        #
        x = self.messages.waitForReceivedMsgInThisThread()
        _link = x.find_element("tag name", "a")
        self.actions = Actions(self.marionette)
        self.actions.long_press(_link, 2).perform()

        #
        # Check the email address is not a link in edit mode.
        #
        self.UTILS.element.waitForNotElements(("xpath", "//button[text()='Create new contact']"),
                                   "Create new contact button")
        self.messages.createAndSendSMS([self.num1], "Email addy {} test.".format(self.emailAddy))
        x = self.messages.waitForReceivedMsgInThisThread()
