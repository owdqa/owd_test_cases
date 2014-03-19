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
from OWDTestToolkit.apps.contacts import Contacts


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
        # Make sure we have no threads (currently blocked - use _RESTART_DEVICE instead).
        #
        #self.messages.deleteAllThreads()

        #
        # Create and send a new test message.
        #
        self.messages.createAndSendSMS([self.num1], 
                                       "Email {} one, email {} two, email {} three.".format("one@www.test.com", self.emailAddy, "three@www.test.com"))
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Long press the 2nd email link.
        #
        link = x.find_elements("tag name", "a")
        link[1].tap()

        #
        # Click 'create new contact'.
        #
        x = self.UTILS.element.getElement( ("xpath", "//button[text()='Create new contact']"),
                                   "Create new contact button")
        x.tap()

        #
        # Verify that the email is in the email field.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        x = self.UTILS.element.getElement(("id","email_0"), "Email field")
        x_txt = x.get_attribute("value")
        self.UTILS.test.TEST(x_txt == self.emailAddy, "Email is '" + self.emailAddy + "' (it was '" + x_txt + "')")