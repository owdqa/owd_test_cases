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

class test_19247(GaiaTestCase):
    _Description = "(BLOCKED BY BUG 879816) [CAMERA] Delete a picture just taken."
    
    def setUp(self):
        #
        # Set up child objects.
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.camera     = Camera(self)
        self.gallery    = Gallery(self)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Record a test video.
        #
        self.camera.launch()
        self.camera.takePicture()
 
        #
        # Tap the thumbnail for it (assume it's the only one).
        #
        self.camera.clickThumbnail(0)
         
        #
        # Tap the trash icon.
        #
        x = self.UTILS.getElement( ("id", "delete-button"), "Trash icon")
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
        
        # A nice additional check, but currently fails a lot due to the 'gallery has no thumbnails'
        # issue. It's not strictly part of this test, so leave it commented out for now.
#         #
#         # Launch the Gallery app.
#         #
#         self.gallery.launch()
#         
#         #
#         # Check all is as it should be.
#         #
#         self.UTILS.waitForElements(DOM.Gallery.no_thumbnails_message, "Message saying there are no photos or videos", True, 5)
#         self.UTILS.waitForNotElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails", True, 5)
