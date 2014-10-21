#===============================================================================
# 29914: Verify that when sending a mms to multiple recipients (contacts),
# only a new thread will be created for the message
#
# Pre-requisites:
# Contacts imported from different sources (facebook, gmail, hotmail, SIM
# card) into the addressbook
#
# Procedure:
# 1. Open SMS app
# 2. Tap on new to create a new MMS(attach a file)
# 3. Tap on '+' icon to add a recipient. Repeat this step several times
# selecting contacts from different sources (ER1)
# 4. Type some characters and tap on Send (ER2)
# 5. Look at the Inbox (ER3)
#
# Expected results:
# ER1. All the recipients are correctly added
# ER2. The message is sent to all the recipients
# ER3. On the inbox view there would be only one MMS thread for the
# multi-recipient MMS sent
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

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
        self.test_nums = ["1111111", "2222222", "333333333", "444444444"]
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

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
        self.gallery.click_on_thumbnail_at_position_mms(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()

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
        self.UTILS.reporting.logResult("info", "Number of threads {} in list.".format(original_count))
        self.UTILS.test.TEST(original_count == 1, "Check how many threads are there")
