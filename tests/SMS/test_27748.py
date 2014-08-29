#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages

class test_main(GaiaTestCase):

    _RESTART_DEVICE = True

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

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        # Make sure we have no threads (currently blocked - use _RESTART_DEVICE instead).
        #
        self.messages.launch()
#         self.messages.deleteThreads([self.phone_number])
  
        #
        # Send a message to create a thread (use number, not name as this
        # avoids some blocking bugs just now). 
        #
        self.messages.createAndSendSMS([self.phone_number], "Test 1")
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
  
        self.messages.enterSMSMsg("Test 2")
        self.messages.sendSMS()
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
  
        self.messages.enterSMSMsg("Test 3")
        self.messages.sendSMS()
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
  
        #
        # Leave this thread.
        #
        self.messages.closeThread()
 
        #
        # Enter the thread.
        #
        self.messages.openThread(self.phone_number)
 
        #
        # Find the first message.
        #
        x = self.UTILS.element.getElements(DOM.Messages.message_list, "Message list", False)
        pos = 0
        for i in x:
            if i.find_element("xpath", "//p[text()='Test 1']"):
                break
            pos += 1

        #
        # Now verify that the order is as expected.
        #

        for i in range(3):
            self.checkMsg(x, pos, "Test {}".format(i + 1), "outgoing")
            pos += 1
            self.checkMsg(x, pos, "Test {}".format(i + 1), "incoming")
            pos += 1
 
        #
        # Tap the message area.
        #
        x = self.UTILS.element.getElement(DOM.Messages.input_message_area, "Message area")
        x.tap()

        #
        # Check the keyboard is now present.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Keyboard.frame_locator)

    def checkMsg(self, p_list, p_pos, p_str, p_direction):
        #
        # Do the check of each message.
        #
        self.UTILS.test.TEST(p_list[p_pos].find_element("xpath", ".//p").text == p_str,
                        "The messages at position " + str(p_pos) + " contains the string '" + p_str + "'.")

        self.UTILS.test.TEST(p_direction in p_list[p_pos].get_attribute("class"),
                        "The message at position " + str(p_pos) + " is '" + p_direction + "'.")






