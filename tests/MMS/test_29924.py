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


    def tearDown(self):
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
        # Insert image in the device
        #
        self.UTILS.general.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

        #
        # Attach an image file
        #
        attach = self.UTILS.element.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        #
        # Select a image from gallery
        #
        gallery = self.UTILS.element.getElement(DOM.Messages.mms_from_gallery, "From gallery")
        gallery.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Gallery.frame_locator)
        self.gallery.clickThumbMMS(0)


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

