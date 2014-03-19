#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery

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
        self.gallery = Gallery(self)

        #
        # Establish which phone number to use.
        #
        self.target_telNum = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.target_telNum)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        #
        # Load an image file into the device.
        #
        self.UTILS.general.addFileToDevice('./tests/_resources/80x60.jpg',
                                    destination='DCIM/100MZLLA')

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
        self.messages.addNumbersInToField([self.target_telNum])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self.test_msg)
        self.messages.createMMSImage()
        self.gallery.clickThumbMMS(0)

        #
        # add subject
        #
        self.messages.addSubject(self.test_subject)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()

        #
        # This step is necessary because our sim cards receive mms with +XXX
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.openThread("+" + self.target_telNum)

        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.messages.waitForReceivedMsgInThisThread()
        self.UTILS.test.TEST(returnedSMS, "A receieved message appeared in the thread.", True)

        #
        #  Forward a message in this case we use "mmssub" to send a mms with subject.
        #
        self.messages.fordwardMessage("mmssub", self.target_telNum)

