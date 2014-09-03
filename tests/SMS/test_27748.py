#===============================================================================
# 27748: Verify the textfield item
#
# Pre-requisites:
# The device has some SMS conversation (sent and received)
#
# Procedure:
# 1- Open SMS app
# 2. Enter in the detail of a conversation
# RES-1
# 3. Click on the text field item
# RES-2
#
# Expected results:
# RES-1: Users can view the details of a conversation, in which all the
# messages exchanged are displayed.
# RES-2: The keyboard is loaded
#===============================================================================
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        #
        # Import contact (adjust the correct number).
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.data_layer.delete_all_sms()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Send some messages to create a thread
        #
        self.texts = ["Test 1", "Test 2", "Test 3"]
        self.directions = ["outgoing", "incoming"]
        self.create_test_sms(self.phone_number, self.texts)

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Enter the thread.
        #
        self.messages.openThread(self.phone_number)

        #
        # Find the first message.
        #
        time.sleep(2)
        msg_list = self.UTILS.element.getElements(DOM.Messages.message_list, "Message list", False)
        self.UTILS.debug.savePageHTML('/tmp/tests/test_123/messages.html')
        msgs = [(text, direction) for text in self.texts for direction in self.directions]
        for (msg, expected) in zip(msg_list, msgs):
            direction = "outgoing" if "outgoing" in msg.get_attribute("class") else "incoming"
            text = self.marionette.find_element('css selector', '.message-body p', id=msg.id).text
            self.UTILS.test.TEST(text == expected[0], "**** Text: {}  Expected: {}".format(text, expected[0]))
            self.UTILS.test.TEST(direction == expected[1], "Direction: {}  Expected: {}".\
                                 format(direction, expected[1]))
        #
        # Tap the message area.
        #
        x = self.UTILS.element.getElement(DOM.Messages.input_message_area, "Message area")
        x.tap()

        #
        # Check the keyboard is now present.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Keyboard.frame_locator)

    def create_test_sms(self, number, msg_list):
        """Send messages in the list to populate a thread.
        """
        for msg in msg_list:
            self.data_layer.send_sms(number, msg)
            self.UTILS.statusbar.wait_for_notification_toaster_detail(msg, timeout=120)
