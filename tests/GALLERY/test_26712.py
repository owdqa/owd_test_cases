#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.utils import UTILS
import time


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)
        self.camera = Camera(self)
        self.UTILS.setPermission('Camera', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Open the gallery application etc...
        #
        self.UTILS.addFileToDevice('./tests/_resources/img1.jpg', destination='DCIM/100MZLLA')
        self.gallery.launch()

        self.gallery.waitForThumbnails(1)

        before_pics = len(self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails"))
        self.UTILS.logResult("info", "Before photo taken, we have %s thunbnails." % before_pics)

        x = self.UTILS.getElement(DOM.Gallery.camera_button, "Camera button")
        x.tap()

        time.sleep(5)

        self.UTILS.switchToFrame(*DOM.Camera.frame_locator)

        self.camera.takePicture()

        self.camera.goToGallery()

        time.sleep(3)

        after_pics = len(self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails"))
        self.UTILS.TEST(after_pics == (before_pics + 1), "After photo taken, we have {} thunbnails (there were {}).".\
                        format(before_pics + 1, after_pics))
