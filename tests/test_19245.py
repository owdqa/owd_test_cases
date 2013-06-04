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
import time

class test_19245(GaiaTestCase):
    _Description = "[CAMERA] Delete a video just recorded."
    
    def setUp(self):
        #
        # Set up child objects.
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.camera     = AppCamera(self)
        self.gallery      = AppGallery(self)
        
    
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Record a test video.
        #
        self.camera.launch()

        #
        # record a 5 second video.
        #
        self.camera.recordVideo(5)
 
        #
        # Tap the thumbnail for it (assume it's the only one).
        #
        self.camera.clickThumbnail(0)
         
        #
        # Tap the trash icon.
        #
        x = self.UTILS.getElement(DOM.Camera.trash_icon, "Trash icon", True, 10, True)
        x.tap()
         
        #
        # Tap OK in the confirmation dialog.
        #
        myIframe = self.UTILS.currentIframe()
         
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement( ("id", "modal-dialog-confirm-ok"), "Confirm deletion button")
        x.tap()
         
        self.UTILS.switchToFrame("src", myIframe)
         
        #
        # Verify that there are no more thumbnails.
        #
        self.UTILS.waitForNotElements(DOM.Camera.thumbnail, "Camera thumbnails")
        
        #
        # Launch the Gallery app.
        #
        self.gallery.launch()
        
        #
        # Check all is as it should be.
        #
        self.UTILS.waitForElements(DOM.Gallery.no_thumbnails_message, "Message saying there are no thumbnails", True, 5)
        self.UTILS.waitForNotElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails", True, 5)
