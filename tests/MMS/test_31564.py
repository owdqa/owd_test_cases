#===============================================================================
# 31564: Cancel adding a subject in new message/multimedia message
#
# Procedure:
# 1. Open Messaging/multimedia message app
# 2. Create a new message/multimedia message
# 3.Tap on the top-right icon to show the options menu (ER1)
# 4. Tap on Cancel (ER2)
#
# Expected result:
# ER1. It appears a screen giving options to Add subject and Cancel
# ER2. User is taken back to the compose message view from which the
# Add subject screen was launched
#===============================================================================

from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    test_msg = "Hello World"
    test_subject = "My Subject"

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()

        # Create a new SMS
        self.messages.startNewSMS()

        # Insert the phone number in the To field
        self.messages.addNumbersInToField([self.phone_number])

        # Create MMS.
        self.messages.enterSMSMsg(self.test_msg)

        # Add subject
        self.messages.addSubject(self.test_subject)

        # Press cancel options button
        self.messages.cancelSettings()

        # Review settings options button
        self.UTILS.reporting.logResult("info", "Cliking on messages options button")
        options_btn = self.UTILS.element.getElement(DOM.Messages.messages_options_btn,
            "Messages option button is displayed")

        self.UTILS.test.test(options_btn, "Settings options.", True)
