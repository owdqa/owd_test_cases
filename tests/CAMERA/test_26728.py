# OWD-26728: Go to Gallery from Camera
# ** Procedure
#       1- Open Camera app 
#       2- Using the dedicated key/buttom, go to Gallery 
#       3- Check that Gallery is correctly open 
#       4- Check that Camera app remains in backgroud
# ** Expected Results
#       It is possible to go to Gallery from Camera app. The device is able to leave Camera app in background while being in Gallery

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
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        self.camera.launch()
        self.camera.take_picture()
        self.camera.open_preview()
        self.camera.go_to_gallery()

        current_thumbs = self.gallery.get_number_of_thumbnails()
        self.UTILS.test.test(current_thumbs == self.previous_thumbs + 1,
                             "After taking a picture, there's one item more in the gallery")


        # Check Camera is running in the background.
        self.UTILS.home.holdHomeButton()
        x = self.UTILS.element.getElement((DOM.Home.app_card[0], DOM.Home.app_card[1].format("camera")),
                                  "When home button is held, camera 'card'", False)
