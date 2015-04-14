# OWD-26328: Make a video recording - verify the recording is successful and added to the gallery
# ** Procedure
#       1. Open camera app
#       2. Select video option
#       3. Record a video
#       4. Press home button
#       5. Open Gallery app
# ** Expected Results
#       The video is added in the gallery app

import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.apps.gallery import Gallery


class test_main(FireCTestCase):

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)
        self.camera = Camera(self)

        self.UTILS.app.setPermission('Camera', 'geolocation', 'deny')
        self.video_duration = 5

        self.gallery.launch()
        time.sleep(2)
        self.previous_thumbs = self.gallery.get_number_of_thumbnails()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.camera.launch()
        self.camera.take_video(self.video_duration)
        self.camera.open_preview()

        self.gallery.launch()
        current_thumbs = self.gallery.get_number_of_thumbnails()
        self.UTILS.test.test(current_thumbs == self.previous_thumbs + 1,
                             "After taking a picture, there's one item more in the gallery")

        # Open the first thumbnail (should be our video).
        self.gallery.click_on_thumbnail_at_position(0)
        self.gallery.check_video_length(self.video_duration)
