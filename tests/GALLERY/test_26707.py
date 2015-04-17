# OWD-26707: Delete a picture
# ** Procedure
#       1- Open Gallery app
#       2- Select a picture
#       3- Delete the selected picture
#       4- Close Gallery app
# ** Expected Results
#    The picture is correctly deleted so it is not shown in Gallery app anymore
import time
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.utils.utils import UTILS


class test_main(PixiTestCase):

    def setUp(self):
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)

        self.gallery.launch()
        time.sleep(2)
        self.previous_thumbs = self.gallery.get_number_of_thumbnails()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.general.add_file_to_device('./tests/_resources/img1.jpg', destination='DCIM/100MZLLA')
        self.gallery.launch()
        self.gallery.wait_for_thumbnails_number(1)
        self.gallery.delete_thumbnails([0])

        current_thumbs = self.gallery.get_number_of_thumbnails()
        self.UTILS.test.test(current_thumbs == self.previous_thumbs + 1,
                             "After taking a picture, there's one item more in the gallery")
