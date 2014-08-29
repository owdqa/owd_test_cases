#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from tests._mock_data.contacts import MockContact

class test_main(GaiaTestCase):

   #
    # Restart device to starting with wifi and 3g disabled.
    #
    _RESTART_DEVICE = True


    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.test_msg = "Hello World"

        #
        # Establish which phone number to use.
        #
        self.test_nums = ["1111111", "2222222","333333333","444444444"]


    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        #
        for num in self.test_nums:
            self.messages.addNumbersInToField([num])

        #
        # Create MMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Add an image file
        #
        self.UTILS.general.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

        self.messages.createMMSImage()
        self.gallery.clickThumbMMS(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        #time.sleep(5)

        #
        # Obtaining file attached type
        #
        x = self.UTILS.element.getElement(DOM.Messages.attach_preview_img_type, "preview type")
        typ = x.get_attribute("data-attachment-type")

        if typ != "img":
            self.UTILS.test.quitTest("Incorrect file type. The file must be img ")


        #
        # Check how many elements are there
        #
        self.UTILS.reporting.logResult("info", "Check how many threads are there")
        original_count = self.messages.countNumberOfThreads()
        self.UTILS.reporting.logResult("info",
                             "Number of threads " + str(original_count) +
                              " in list.")
        self.UTILS.test.TEST(original_count == 1, "Check how many threads are there")
        
        self.UTILS.reporting.logResult("info", "Test correctly finished")