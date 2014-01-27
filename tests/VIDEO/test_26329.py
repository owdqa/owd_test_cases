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
        # Set up child objects.
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.camera     = Camera(self)
        self.video      = Video(self)

        self.UTILS.setPermission('Camera', 'geolocation', 'deny')
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Record a test video.
        #
        self.camera.launch()
        self.camera.recordVideo(5)
        self.camera.checkVideoLength(0, 3, 6)

        #
        # Open the video player application.
        #
        self.video.launch()
        time.sleep(5)
         
        #
        # the first thumbnail should be our video.
        #
        self.video.checkThumbDuration(0, "00:05", 2)
         
        #
        # Check that the video is as long as expected.
        #
        self.video.checkVideoLength(0, 3, 6)