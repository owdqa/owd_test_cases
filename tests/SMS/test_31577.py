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
from marionette import Actions
from tests._mock_data.contacts import MockContact

class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)

        self.actions = Actions(self.marionette)

        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending sms to telephone number " + self.target_telNum)

        #
        # Prepare the contact we're going to insert.
        #
        self.num1 = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel = {'type': '', 'value': self.num1})
        self.UTILS.general.insertContact(self.contact)


    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Sometimes causes a problem if not cleared.
        #
        self.UTILS.statusbar.clearAllStatusBarNotifs()

        #
        # Create message - 5 x 10 chars.
        #
        sms_message = "0123456789" * 5
        self.UTILS.reporting.logComment("Message length sent: {}".format((len(sms_message))))

        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create and send a new test message. Repeat this steps to having several sms in the thread
        #
        self.messages.createAndSendSMS([self.target_telNum], sms_message)

        #
        # Wait for the last message in this thread to be a 'received' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.test.TEST(returnedSMS, "A received message appeared in the thread.", True)

        self.messages.forwardMessageToContact("sms", self.contact["name"])



