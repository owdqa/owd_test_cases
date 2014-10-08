#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
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

        self.UTILS.app.setPermission('Camera', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Start the camera application.
        #
        self.camera.launch()

        #
        # Take a video.
        #
        self.camera.take_video(5)
        self.camera.check_video_length(0, 3, 7)

        #
        # Open the gallery application.
        #
        self.UTILS.home.goHome()
        self.gallery.launch()

        #
        # Open the first thumbnail (should be our video).
        #
        self.gallery.clickThumb(0)
        self.gallery.check_video_length(3, 7)
