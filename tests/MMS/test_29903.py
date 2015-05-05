#===============================================================================
# 29903: Verify that all the MMSs in a thread are chronologically ordered
#
# Procedure:
# On DuT create an MMS thread by sending/receiving MMSs to/from the same number
#
# Expected results:
# All the MMSs in the same thread are correctly ordered no matter the time set
# in one device or the other or the network
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.settings import Settings


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.settings = Settings(self)

        self.test_msg = "Hello World"

        self.phone_number = self.UTILS.general.get_config_variable("incoming_call_number", "common")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.messages.launch()

        # Create and Send all MMS
        for msg in ["Test {}".format(i) for i in range(3)]:
            self.messages.create_and_send_mms("image", [self.phone_number], msg)
            self.messages.closeThread()

        self.messages.openThread(self.phone_number)

        # Check the messages
        msg_list = self.UTILS.element.getElements(DOM.Messages.message_list, "Message list", False)
        pos = 0
        for (pos, msg) in enumerate(msg_list):
            # Do the check for each message.
            self.UTILS.test.test(msg.find_element("css selector", "p span").text == "Test {}".format(pos),
                        "The message at position {} contains the string 'Test {}'.".format(pos, pos))
            self.UTILS.test.test("outgoing" in msg.get_attribute("class"),
                        "The message at position {} is  outgoing.".format(pos))
