#===============================================================================
# 31571: Forward an MMS to multiple recipients
#
# Pre-requisites:
# There is at least one MMS in the message app
# There is at least one contact in the contact list
#
# Procedure:
# 1. Open Messaging app
# 2. Open the MMS
# 3. Long press on it (ER1)
# 4. Tap on Forward message option (ER2)
# 5. Tap on '+' icon to select a contact (ER3)
# 6. Tap on a contact (ER4)
# 7. Now, tap on 'To' field and add a phone number manually (ER5)
# 8. Tap on Send key (ER6)
#
# Expected result:
# ER1. Message module options menu is shown
# ER2. New message composer screen is shown with the message to be forwarded
# in the text field. The 'To' field is empty.
# ER3. The list of contacts is shown
# ER4. The contact is added into the 'To' field
# ER5. The number is added into the 'To' field
# ER6. The message is sent correctly
#===============================================================================

import sys
sys.path.insert(1, "./")
from gaiatest  import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from tests._mock_data.contacts import MockContact


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
        self.target_mms_number = self.UTILS.general.get_os_variable("TARGET_MMS_NUM")

        #
        # Prepare the contact we're going to insert.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact = MockContact(tel={'type': '', 'value': self.phone_number})
        self.UTILS.general.insertContact(self.contact)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Load an image file into the device.
        #
        self.UTILS.general.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

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
        self.messages.createMMSImage()
        self.gallery.clickThumbMMS(0)

        #
        # Click send and wait for the message to be received
        #
        self.messages.sendSMS()
        self.UTILS.statusbar.wait_for_notification_toaster_title(self.target_mms_number, timeout=120)
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.messages.openThread(self.target_mms_number)

        self.messages.forwardMessageToMultipleRecipients("mms", self.target_mms_number, self.contact["name"])
