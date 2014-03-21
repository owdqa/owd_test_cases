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
import time


class test_main(GaiaTestCase):

    num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Start with no SMS.
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Send a message to an invalid number to create a thread with just an
        # outgoing message..
        #
        msg_text = str(time.time())
        self.messages.createAndSendSMS([self.num], msg_text)

        #
        # Return to the threads view.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Get the preview txt for our test.
        #
        preview_text = self.messages.getThreadText(self.num)

        self.UTILS.test.TEST(preview_text in msg_text,
                        "Preview text ({}) is in the original message text({}).".format(preview_text, msg_text))
