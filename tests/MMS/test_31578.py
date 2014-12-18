#===============================================================================
# 31578: Forward an MMS which is in a thread with more messages to a phone number
#
# Pre-requisites:
# There should be a thread created with several sent/received multi-media messages
#
# Procedure:
# 1. Open Messaging app
# 2. Open the thread and select an MMS
# 3. Long press on it (ER1)
# 4. Tap on Forward message option (ER2)
# 5. Introduce a phone number in the 'To' field
# 6. Tap on Send key (ER3)
#
# Expected results:
# ER1. Message module options menu is shown
# ER2. New message composer screen is shown with the message to be forwarded in the
# text field. The 'To' field is empty.
# ER3. The message is sent correctly
#===============================================================================

from gaiatest  import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

    test_msg = "Hello World"

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
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Load an image file into the device.
        #
        self.UTILS.general.add_file_to_device('./tests/_resources/80x60.jpg')

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
        self.messages.create_mms_image()
        self.gallery.click_on_thumbnail_at_position_mms(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        self.messages.wait_for_message()
        self.messages.forwardMessage("mms", self.phone_number)
