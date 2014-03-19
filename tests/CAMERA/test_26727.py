#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.apps.gallery import Gallery

#
# Imports particular to this test case.
#


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects.
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.camera = Camera(self)
        self.gallery = Gallery(self)

        self.UTILS.app.setPermission('Camera', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Record a test video.
        #
        self.camera.launch()
        self.camera.takePicture()

        #
        # Tap the thumbnail for it (assume it's the only one).
        #
        self.camera.clickThumbnail(0)

        #
        # Tap the trash icon.
        #
        x = self.UTILS.element.getElement(DOM.Camera.trash_icon, "Trash icon")
        x.tap()

        #
        # Tap OK in the confirmation dialog.
        #
        myIframe = self.UTILS.iframe.currentIframe()

        self.marionette.switch_to_frame()
        x = self.UTILS.element.getElement(DOM.GLOBAL.modal_confirm_ok, "Confirm deletion button")
        x.tap()

        self.UTILS.iframe.switchToFrame("src", myIframe)

        #
        # Verify that there are no more thumbnails.
        #
        self.UTILS.element.waitForNotElements(DOM.Camera.thumbnail, "Camera thumbnails")
