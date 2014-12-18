from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages

class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.phone_number)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()

        # Start a new sms.
        self.messages.startNewSMS()

        # Enter a message the message area.
        x = self.messages.enterSMSMsg("Test text.")

        # Check the 'Send button isn't enabled yet.
        x = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send message button")
        self.UTILS.test.test(not x.is_enabled(), 
                        "Send button is not enabled after message supplied, but target still empty.")

