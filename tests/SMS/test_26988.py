# OWD-26988: Accept Adding the phone number to an existing contact
# ** Procedure
#         1. Open the SMS
#         2. On the thread view tap on the header where the number is shown
#         3. Then tap on ' Add to an existing contact' option
#         4. When the contact list is shown, tap on any of them
#         5. Tap on Done
# ** Expected Results
#         The contact should be modified (phone number is added to existing contact)
#         and the user is returned to the SMS thread view screen,
#         where the header is updated according to the modified contact.
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # Launch messages app.
        self.messages.launch()

        # Create and send a new test message.
        self.messages.create_and_send_sms([self.phone_number], "Test message.")
        self.messages.wait_for_message()

        # Tap the header to create a contact.
        self.messages.header_addToContact()

        # Select our contact.
        self.contacts.view_contact(self.contact["givenName"], False)

        # Check the phone number.
        second_phone = self.UTILS.element.getElement(("id", "number_1"), "2nd phone number.")
        self.UTILS.test.test(second_phone.get_attribute("value") == self.phone_number,
                             "Contact now has a 2nd number which is '{}' (it was '{}').".format(self.phone_number, second_phone.get_attribute("value")))

        # Press the Done button.
        done_btn = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "Update button")
        done_btn.tap()

        # Wait for contacts app to close and return to sms app.
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src, '{}')]".format(DOM.Contacts.frame_locator[1])),
                                              "Contacts iframe")

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        # Verify the header is now the name,
        header = self.UTILS.element.getElement(DOM.Messages.message_header, "Message header")
        self.UTILS.test.test(header.text == self.contact["name"],
                             "Message header has been changed to match the contact (it was '{}').".format(header.text))

        # Go back to the threads view and check the message name there too.
        self.messages.go_back()
        self.messages.openThread(self.contact["name"])
