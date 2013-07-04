#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase
from OWDTestToolkit import *

#
# Imports particular to this test case.
#

class test_main(GaiaTestCase):
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.gallery    = Gallery(self)
        self.camera     = Camera(self)

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Start the camera application.
        #
        self.camera.launch()
        
        #
        # Take a video.
        #
        self.camera.recordVideo(5)
        self.camera.checkVideoLength(0, 4, 6)
        
        #
        # Open the gallery application.
        #
        self.UTILS.goHome()
        self.gallery.launch()

        #
        # Open the first thumbnail (should be our video).
        #
        self.gallery.clickThumb(0)
        self.gallery.checkVideoLength(4, 6)
