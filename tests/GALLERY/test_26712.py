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
import os, time

class test_main(GaiaTestCase):
    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.gallery    = Gallery(self)
        self.camera     = Camera(self)

        self.UTILS.setPermission('Camera', 'geolocation', 'deny')
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Open the gallery application etc...
        #
        self.UTILS.addFileToDevice('./tests/_resources/img1.jpg', destination='DCIM/100MZLLA')
        self.gallery.launch()
        
        self.gallery.waitForThumbnails(1)
        
        _beforePic = len(self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails"))
        self.UTILS.logResult("info", "Before photo taken, we have %s thunbnails." % _beforePic)
        
        x = self.UTILS.getElement(DOM.Gallery.camera_button, "Camera button")
        x.tap()
        
        self.UTILS.switchToFrame(*DOM.Camera.frame_locator)
        
        self.camera.takePicture()
        
        self.camera.goToGallery()
              
        _afterPic = len(self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails"))
        self.UTILS.TEST(_afterPic == (_beforePic+1), "After photo taken, we have %s thunbnails (there was %s)." % \
                        (_beforePic+1, _afterPic))

#         x = self.UTILS.screenShotOnErr()
#         self.UTILS.logResult("info", "x", x)
