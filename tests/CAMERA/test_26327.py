#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.apps import Gallery

#
# Imports particular to this test case.
#


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)
        self.camera = Camera(self)

        self.UTILS.setPermission('Camera', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Start the camera application.
        #
        self.camera.launch()

        #
        # Take a picture.
        #
        self.camera.takePicture()

        #
        # Get a screenshot of the camera at this stage.
        #
        self.camera.clickThumbnail(0)

        #
        # Open the gallery application.
        #
        self.gallery.launch()

        #
        # Check we have at least 1 picture in the thumbnails.
        #
        self.UTILS.TEST(self.gallery.thumbCount() > 0, "At least one thumbnail is present in gallery.")

        #
        # Open the image (0 should be ours since we just added it!).
        #
        self.gallery.clickThumb(0)
