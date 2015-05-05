# OWD-26712: Tap on Camera option to open Camera app
# ** Procedure
#       1- Open Gallery app
#       2- Look at the main screen looking for the Camera key
#       3- Tap on Camera key
#       4- Check if camera app is open
#       5- In that case, take a picture
#       6- Check that the picture taken is already in Gallery app
#       7- Close Gallery app
# ** Expected Results
#       It is possible to open Camera app and take a picture by pressing Camera key/icon in Gallery app
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.utils.utils import UTILS
import time


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)
        self.camera = Camera(self)
        self.UTILS.app.setPermission('Camera', 'geolocation', 'deny')
        self.UTILS.general.add_file_to_device('./tests/_resources/img1.jpg')

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.gallery.launch()

        self.gallery.wait_for_thumbnails_number(1)

        before_pics = len(self.UTILS.element.getElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails"))
        self.UTILS.reporting.logResult("info", "Before photo taken, we have {} thumbnails.".format(before_pics))

        camera_btn = self.UTILS.element.getElement(DOM.Gallery.thumbnail_camera_button, "Camera button")
        camera_btn.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Camera.frame_locator)
        self.camera.take_picture()
        self.camera.open_preview()
        self.camera.go_to_gallery()

        after_pics = len(self.UTILS.element.getElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails"))
        self.UTILS.test.test(after_pics == before_pics + 1, "After photo taken, we have {} thunbnails".format(after_pics))
