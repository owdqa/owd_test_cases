from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.apps.video import Video
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.utils.utils import UTILS
import time


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects.
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.camera = Camera(self)
        self.video = Video(self)

        self.UTILS.app.setPermission('Camera', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        # Record a test video.
        self.camera.launch()
        rec_length = self.camera.take_video(6)
        self.camera.open_preview()
        self.camera.check_video_length(rec_length)

        # Open the video player application.
        self.video.launch()
        time.sleep(2)
        self.video.wait_for_list()

        # the first thumbnail should be our video.
        self.video.check_thumb_duration(0, rec_length)

        # Check that the video is as long as expected.
        self.apps.kill_all()
        time.sleep(2)
        self.video.launch()
        self.video.check_video_length(0, rec_length)
