#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.utils.utils import UTILS


class test_main(GaiaTestCase):

    img_list = ('img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg')

    img_sizes = (68056, 51735, 47143, 59955, 60352)

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)

    def tearDown(self):
        for img in self.img_list:
            self.UTILS.general.remove_file(img, 'DCIM/100MZLLA/')
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Load sample images into the gallery.
        #
        for img in self.img_list:
            self.UTILS.general.addFileToDevice('./tests/_resources/' + img, destination='DCIM/100MZLLA')

        #
        # Open the gallery application.
        #
        self.gallery.launch()

        #
        # Takes a few seconds for the thumbs to appear...
        #
        self.gallery.waitForThumbnails(len(self.img_list))
