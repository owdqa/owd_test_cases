from gaiatest import GaiaTestCase

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

        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

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
        self.messages.create_and_send_sms([self.phone_number], "Test message.")
        x = self.messages.wait_for_message()

        #
        # Tap the header to create a contact.
        #
        self.messages.header_createContact()

        #
        # Fill in some details.
        #
        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields['givenName'], "Test")
        self.contacts.replace_str(contFields['familyName'], "Testerton")

        #
        # Press the Done button.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.done_button, "Done button")
        x.tap()

        #
        # Wait for contacts app to close and return to sms app.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath",
            "//iframe[contains(@src, '{}')]".format(DOM.Contacts.frame_locator[1])),
                                       "Contacts iframe")

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        #
        # Verify the header is now the name,
        #
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Message header")
        self.UTILS.test.test(x.text == "Test Testerton", 
                        "Message header has been changed to match the contact (it was '{}').".format(x.text))

        #
        # Go back to the threads view and check the message name there too.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.messages.openThread("Test Testerton")