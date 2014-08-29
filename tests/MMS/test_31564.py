#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    test_msg = "Hello World"
    test_subject = "My Subject"

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.target_mms_number = self.UTILS.general.get_os_variable("TARGET_MMS_NUM")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):


        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.messages.addNumbersInToField([self.phone_number])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Add subject
        #
        self.messages.addSubject(self.test_subject)


        #
        # Press cancel options button
        #
        self.messages.cancelSettings()

        #
        # Review settings options button
        #
        self.UTILS.reporting.logResult("info", "Cliking on messages options button")
        x = self.UTILS.element.getElement(DOM.Messages.messages_options_btn,
            "Messages option button is displayed")

        self.UTILS.test.TEST(x, "Settings options.", True)

        self.UTILS.reporting.logResult("info",
                             "Test working")