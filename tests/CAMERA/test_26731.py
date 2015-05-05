# OWD-26731: Delete a video just recorded
# ** Procedure
#       1. Open camera app
#       2. Switch to video mode
#       3. Start the recording
#       4. After some seconds stop it
#       5. Tap in the preview icon in the left upper corner
#       6. Tap in the trash icon in the right down corner
#       7. Tap in the OK button in the confirmation screen
# ** Expected Results
#       The video is not saved and you cannot see it in the gallery.

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.apps.gallery import Gallery


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.camera = Camera(self)
        self.gallery = Gallery(self)

        self.UTILS.app.setPermission('Camera', 'geolocation', 'deny')

        self.gallery.launch()
        time.sleep(2)
        self.previous_thumbs = self.gallery.get_number_of_thumbnails()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.camera.launch()
        self.camera.take_video(5)
        self.camera.open_preview()
        self.camera.delete_from_preview()

        self.gallery.launch()
        time.sleep(2)
        current_thumbs = self.gallery.get_number_of_thumbnails()

        self.UTILS.test.test(current_thumbs == self.previous_thumbs,
                             "After taking a picture and delete it, we remain the same")
