#===============================================================================
# 29924: Click remove picture button in attached file options from a
# picture attached
#
# Procedure:
# 1. Open sms app
# 2. press new sms/mms button
# 3. attach a image file
# 4. tap on the image attached
# 5. Press remove button
#
# Expected results:
# The file is removed successfully
#===============================================================================

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.gallery import Gallery


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.gallery = Gallery(self)
        self.UTILS.general.add_file_to_device('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')
        self.test_msg = "This is a test message"

    def tearDown(self):
        self.UTILS.general.remove_file('80x60.jpg', 'DCIM/100MZLLA')
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Launch messages app.
        #
        self.messages.launch()

        #
        # Create a new SMS
        #
        self.messages.startNewSMS()

        self.messages.enterSMSMsg(self.test_msg)

        self.messages.create_mms_image()
        self.gallery.click_on_thumbnail_at_position_mms(0)

        #
        # Open attached file options
        #
        x = self.UTILS.element.getElement(DOM.Messages.attach_preview_img_type, "Open attached file options")
        x.tap()

        #
        # Remove attached file
        #
        x = self.UTILS.element.getElement(DOM.Messages.attached_opt_remove, "Remove attached file")
        x.tap()

        self.UTILS.element.waitForNotElements(DOM.Messages.attach_preview_img_type, "attached file has been removed")
