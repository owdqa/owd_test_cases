# OWD-26327: Take a picture with camera - verify the picture is successfully taken and added to the gallery
# ** Procedure
#       1. Open camera app
#       2. Take a photo
#       3. Press home button
#       4. Open Gallery app
#       ER1
#       5. Open camera app
#       6. Take a photo
#       7. Press on the thumbnail
#       ER2
# ** Expected Results
#       ER1 The photo is added in the gallery app
#       ER2 The photo is opened

import time
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.apps.gallery import Gallery


class test_main(PixiTestCase):

    def setUp(self):
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)
        self.camera = Camera(self)

        self.UTILS.app.setPermission('Camera', 'geolocation', 'deny')

        self.gallery.launch()
        time.sleep(2)
        self.previous_thumbs = self.gallery.get_number_of_thumbnails()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.camera.launch()
        self.camera.take_picture()
        self.camera.open_preview()

        self.gallery.launch()
        current_thumbs = self.gallery.get_number_of_thumbnails()
        self.UTILS.test.test(current_thumbs == self.previous_thumbs + 1,
                     "After taking a picture, there's one item more in the gallery")


        self.gallery.click_on_thumbnail_at_position(0)
