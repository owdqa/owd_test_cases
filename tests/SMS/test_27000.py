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


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)
        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

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
        test_str = "Nine 123456789 numbers."
        self.messages.createAndSendSMS([self.num1], test_str)
        x = self.messages.waitForReceivedMsgInThisThread()

        #
        # Long press the embedded number link.
        #
        y = x.find_element("tag name", "a")  
        y.tap()

        #
        # Select create new contact.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_create_new_contact_btn,
                                    "Create new contact button")
        x.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        contFields = self.contacts.get_contact_fields()

        #
        # Verify the number is in the number field.
        #
        self.UTILS.test.TEST("123456789" in contFields['tel'].get_attribute("value"),
                        "Our target number is in the telephone field (it was {}).".format(contFields['tel'].get_attribute("value")))

        #
        # Put the contact details into each of the fields (this method
        # clears each field first).
        #
        self.contacts.replace_str(contFields['givenName'], "Test2700")
        self.contacts.replace_str(contFields['familyName'], "Testerton")
        x = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        x.tap()

        #
        # Wait for the contacts app to go away.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements( ("xpath", "//iframe[contains(@src, '{}')]".format(DOM.Contacts.frame_locator[1])),
                                       "Contacts iframe")

        #
        # Verify that the sms app is still running.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)