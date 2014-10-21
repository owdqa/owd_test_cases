from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
import time

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        # Start with no SMS.
        self.data_layer.delete_all_sms()

        # Get the correct number for the sms device.
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
        # Send a message to an invalid number to create a thread with just an
        # outgoing message..
        #
        msg_text = str(time.time())
        self.messages.createAndSendSMS([self.phone_number], msg_text)
        self.messages.waitForReceivedMsgInThisThread()
 
        #
        # Return to the threads view.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        #
        # Get the preview txt for our test.
        #
        preview_text = self.messages.getThreadText(self.phone_number)

        self.UTILS.test.TEST(preview_text in msg_text, 
                        "Preview text ({}) is in the original message text({}).".format(preview_text, msg_text))

