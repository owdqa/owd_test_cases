#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.utils import UTILS


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.gallery = Gallery(self)

    def tearDown(self):
        self.UTILS.reportResults()

    def test_run(self):
        #
        # Load sample images into the gallery.
        #
        self.UTILS.addFileToDevice('./tests/_resources/img1.jpg', destination='DCIM/100MZLLA')

        #
        # Open the gallery application.
        #
        self.gallery.launch()

        #
        # Takes a few seconds for the thumbs to appear...
        #
        self.gallery.waitForThumbnails(1)

        #
        # Delete the image.
        #
        self.gallery.deleteThumbnails([0])
