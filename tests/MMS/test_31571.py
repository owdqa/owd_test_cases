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

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.utils.contacts import MockContact


class test_main(FireCTestCase):

    test_msg = "Hello World"

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        #
        # Prepare the contact we're going to insert.
        #
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact(tel={'type': '', 'value': self.phone_number})
        self.UTILS.general.insertContact(self.contact)
        self.data_layer.delete_all_sms()
        self.UTILS.statusbar.clearAllStatusBarNotifs()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Load an image file into the device.
        #
        self.UTILS.general.add_file_to_device('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

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

        self.messages.forwardMessageToMultipleRecipients("mms", self.phone_number, self.contact["name"])
