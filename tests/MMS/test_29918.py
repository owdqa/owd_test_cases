#===============================================================================
# 29918: Verify that the user can attach a file .jpg and it is displayed
# as image
#
# Procedure:
# 1. Open sms app
# 2. press attach button
# 3. Select a file .jpg
# ER1
# 4. Press send button
# ER2
#
# Expected results:
# ER1 The file is attached and is displayed as image in the sms composer
# ER2 The MMS is sends successfully
#===============================================================================

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)

        self.test_msg = "Hello World at {}".format(time.time())

        # Establish which phone number to use.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.UTILS.general.add_file_to_device('./tests/_resources/80x60.jpg')

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()

        # Create a new SMS
        self.messages.startNewSMS()

        # Insert the phone number in the To field
        self.messages.addNumbersInToField([self.phone_number])

        # Create MMS.
        self.messages.enterSMSMsg(self.test_msg)

        self.messages.create_mms_image()
        self.gallery.click_on_thumbnail_at_position_mms(0)
        container = self.UTILS.element.getElement(DOM.Messages.attach_preview_img_type, "Preview of attached image")
        self.UTILS.test.test(container, "Image preview container found")
