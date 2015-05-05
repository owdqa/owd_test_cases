# OWD-26711: Select multiple pictures and delete them 
# ** Procedure
#       1- Open Gallery app
#       2- Using the option given, select multiple pictures
#       3- Delete the selected pictures
#       4- Check that the pictures have been properly removed
#       5- Close Gallery app
# ** Expected Results
#       The pictures are correctly deleted so they are not shown in Gallery app anymore

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.utils.utils import UTILS


class test_main(SpreadtrumTestCase):

    img_list = ('img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg')
    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)

        self.length = len(self.img_list)
        # Load sample images into the gallery.
        for i in self.img_list:
            self.UTILS.general.add_file_to_device('./tests/_resources/' + i)

        self.gallery.launch()
        time.sleep(2)
        self.previous_thumbs = self.gallery.get_number_of_thumbnails()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.gallery.launch()
        self.gallery.wait_for_thumbnails_number(self.length)

        positions_to_delete = (0, 1, 2)
        self.gallery.delete_thumbnails(positions_to_delete)

        current_thumbs = self.gallery.get_number_of_thumbnails()
        self.UTILS.reporting.logResult('info', 'current_thumbs: {}'.format(current_thumbs))
        self.UTILS.reporting.logResult('info', 'previous_thumbs: {}'.format(self.previous_thumbs))
        self.UTILS.test.test(current_thumbs == self.previous_thumbs - len(positions_to_delete),
                             "After deleting {} picture/s we have the rest".format(len(positions_to_delete)))
