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

        self.UTILS.setPermission('Camera', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Start the camera application.
        #
        self.camera.launch()

        #
        # Take a picture.
        #
        self.camera.takePicture()

        #
        # Get a screenshot of the camera at this stage.
        #
        img_thumb_view = self.UTILS.screenShot("_THUMBNAIL_VIEW")
        
        #
        # Open the gallery application.
        #
        self.camera.goToGallery()
        
        #
        # Check we have at least 1 picture in the thumbnails.
        #
        self.UTILS.TEST(self.gallery.thumbCount() > 0, "At least one thumbnail is present in gallery.")
        
        #
        # Check Camera is running in the background.
        #
        self.UTILS.holdHomeButton()
        x = self.UTILS.getElement((DOM.Home.app_card[0], DOM.Home.app_card[1] % "camera"), 
                                  "When home button is held, camera 'card'", False)