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

        self.test_msg = "Hello World at {}".format(time.time())

        #
        # Establish which phone number to use.
        #
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.UTILS.reporting.logComment("Sending mms to telephone number " + self.phone_number)
        self.UTILS.general.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

    def tearDown(self):
        self.UTILS.general.remove_file('80x60.jpg', 'DCIM/100MZLLA')
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
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
        container = self.UTILS.element.getElement(DOM.Messages.attach_preview_img_type)
        self.UTILS.test.TEST(container, "Image preview container found")
