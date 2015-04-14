# OWD-26330: Browse photos in gallery - verify you can see each picture of your sdcard
# ** Procedure
#       1. Insert a SD card with several pictures in the device 
#       2. Open gallery app 
#       3. Browse photos in gallery
# ** Expected Results
#       You can see each picture in your sd card
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.utils.utils import UTILS


class test_main(FireCTestCase):

    img_list = ('img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg')

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)

        self.length = len(self.img_list)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        # Load sample images into the gallery.
        for i in self.img_list:
            self.UTILS.general.add_file_to_device('./tests/_resources/' + i, destination='DCIM/100MZLLA')

        self.gallery.launch()
        self.gallery.wait_for_thumbnails_number(self.length)
        self.gallery.click_on_thumbnail_at_position(0)
        self.gallery.swipe_between_gallery_items(self.length)
