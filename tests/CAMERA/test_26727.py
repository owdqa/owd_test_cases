# 26727: Delete a picture just taken
# ** Procedure
#       1- Open Camera app
#       2- Take a picture
#       3- Delete the picture using the option given for that
#       4- Check that the picture has been removed correctly
# ** Expected Results
#       Using the option to delete a picture from Camera app should work deleting the picture selected
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.apps.gallery import Gallery


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
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
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.camera.launch()
        self.camera.take_picture()
        self.camera.open_preview()
        self.camera.delete_from_preview()

        self.gallery.launch()
        time.sleep(2)
        current_thumbs = self.gallery.get_number_of_thumbnails()

        self.UTILS.test.TEST(current_thumbs == self.previous_thumbs,
                             "After taking a picture and delete it, we remain the same")
