from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts


class test_main(GaiaTestCase):

    test_msg = "Test message."

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        self.num1 = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.num2 = "621234567"

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()

        # Create and send a new test message.
        self.messages.create_and_send_sms([self.num1], "Test {} number.".format(self.num2))
        self.messages.wait_for_message()

        # Tap the header to create a contact.
        self.messages.header_createContact()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        # Cancel the action.
        form_header = self.UTILS.element.getElement(DOM.Contacts.contact_form_header, "Contact form header")
        form_header.tap(25, 25)

        # Wait for the contacts app to go away.
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@src, '{}')]".\
                                               format(DOM.Contacts.frame_locator[1])), "Contacts iframe")

        # Kill the SMS app (and all others).
        self.apps.kill_all()

        # Open the contacts app.
        self.contacts.launch()

        # Verify that there are no contacts.
        self.UTILS.element.waitForElements(("xpath", "//p[contains(text(), 'No contacts')]"),
                                    "No contacts message")
