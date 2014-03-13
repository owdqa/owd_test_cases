#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit.utils import UTILS
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.apps.gallery import Gallery

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
        # Take a video.
        #
        self.camera.recordVideo(5)
        self.camera.checkVideoLength(0, 3, 7)

        #
        # Open the gallery application.
        #
        self.UTILS.goHome()
        self.gallery.launch()

        #
        # Open the first thumbnail (should be our video).
        #
        self.gallery.clickThumb(0)
        self.gallery.checkVideoLength(3, 7)
