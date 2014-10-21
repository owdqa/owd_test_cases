from gaiatest import GaiaTestCase
from OWDTestToolkit.apps.video import Video
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.utils.utils import UTILS
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects.
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.camera = Camera(self)
        self.video = Video(self)

        self.UTILS.app.setPermission('Camera', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # Record a test video.
        self.camera.launch()
        self.camera.take_video(6)
        self.camera.open_preview()
        self.camera.check_video_length(6)

        # Open the video player application.
        self.video.launch()

        # the first thumbnail should be our video.
        self.video.check_thumb_duration(0, 6)

        # Check that the video is as long as expected.
        self.apps.kill_all()
        time.sleep(2)
        self.video.launch()
        self.video.check_video_length(0, 6)
