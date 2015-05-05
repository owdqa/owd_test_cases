from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):
        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        # Prepare the contact we're going to insert.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact(tel={'type': '', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact["tel"]["value"])

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        # Launch messages app.
        self.messages.launch()

        # Type a message containing the required string
        self.messages.startNewSMS()
        self.messages.enterSMSMsg("Test message")
        self.messages.selectAddContactButton()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        # Press the back button.
        self.contacts.go_back()

        self.apps.switch_to_displayed_app()

        # Check 'Send' button is not enabled.
        send_message_button = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send button")
        self.UTILS.test.test(not send_message_button.is_enabled(), "Send button is not enabled.")
