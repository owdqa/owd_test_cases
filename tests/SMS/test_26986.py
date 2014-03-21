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
        self.num2 = "621234567"

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
        self.messages.createAndSendSMS([self.num1], "Test {} number.".format(self.num2))
        self.messages.waitForReceivedMsgInThisThread()

        #
        # Tap the header to create a contact.
        #
        self.messages.header_createContact()

        #
        # Cancel the action.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.edit_cancel_button, "Cancel button")
        x.tap()

        #
        # Wait for the contacts app to go away.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src, '{}')]".\
                                               format(DOM.Contacts.frame_locator[1]), "Contacts iframe"))

        #
        # Kill the SMS app (and all others).
        #
        self.apps.kill_all()

        #
        # Open the contacts app.
        #
        self.contacts.launch()

        #
        # Verify that there are no contacts.
        #
        self.UTILS.element.waitForElements(("xpath", "//p[contains(text(), 'No contacts')]"),
                                    "No contacts message")
