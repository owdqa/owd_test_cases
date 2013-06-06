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

class test_19419(GaiaTestCase):
    _Description = "[BASIC][CAMERA] Take a picture with camera - verify the picture is successfully taken and added to the gallery."
    
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
        # Take a picture.
        #
        self.camera.takePicture()
        
        #
        # TEST: Thumbnail has not been previewed yet.
        #
        prev_marker = self.UTILS.getElement(DOM.Camera.thumbnail_preview_marker, "Thumbnail preview marker", False)
        self.UTILS.TEST((prev_marker.get_attribute("class") == "offscreen"), 
                        "Image is not previewed as soon as picture is taken.")
        
        #
        # Get a screenshot of the camera at this stage.
        #
        self.camera.clickThumbnail(0)
        
        #
        # Open the gallery application.
        #
        self.gallery.launch()
        
        #
        # Check we have at least 1 picture in the thumbnails.
        #
        self.UTILS.TEST(self.gallery.thumbCount() > 0, "At least one thumbnail is present in gallery.")
        
        #
        # Open the image (0 should be ours since we just added it!).
        #
        self.gallery.clickThumb(0)
