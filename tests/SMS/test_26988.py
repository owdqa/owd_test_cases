from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact
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
        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

        self.contact = MockContact()

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
        # Create and send a new test message.
        #
        self.messages.create_and_send_sms([self.phone_number], "Test message.")
        x = self.messages.wait_for_message()

        #
        # Tap the header to create a contact.
        #
        self.messages.header_addToContact()

        #
        # Select our contact.
        #
        self.contacts.view_contact(self.contact["familyName"], False)

        #
        # Check the phone number.
        #
        x = self.UTILS.element.getElement(("id", "number_1"), "2nd phone number.")
        self.UTILS.test.test(x.get_attribute("value") == self.phone_number,
                        "Contact now has a 2nd number which is '{}' (it was '{}').".format(self.phone_number, x.get_attribute("value")))

        #
        # Press the Done button.
        #
        x = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "Update button")
        x.tap()

        #
        # Wait for contacts app to close and return to sms app.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src, '{}')]".format(DOM.Contacts.frame_locator[1])),
                                       "Contacts iframe")

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        #
        # Verify the header is now the name,
        #
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Message header")
        self.UTILS.test.test(x.text == self.contact["name"],
                        "Message header has been changed to match the contact (it was '{}').".format(x.text))

        #
        # Go back to the threads view and check the message name there too.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.messages.openThread(self.contact["name"])