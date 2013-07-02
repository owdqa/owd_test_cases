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
    
    _img_list = ('img1.jpg',
                 'img2.jpg',
                 'img3.jpg',
                 'img4.jpg',
                 'img5.jpg')
                 
    _img_sizes = (68056,51735,47143,59955,60352)

    
    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.gallery    = Gallery(self)

        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        #
        # Load sample images into the gallery.
        #
        for i in self._img_list:
            self.UTILS.addFileToDevice('./tests/_resources/' + i, destination='DCIM/100MZLLA')
            
        #
        # Open the gallery application.
        #
        self.gallery.launch()
        
        #
        # Takes a few seconds for the thumbs to appear...
        #
        self.gallery.waitForThumbnails(len(self._img_list))
        
        # Problemtic - commented out for now.
#         #
#         # Open each picture ...
#         #
#         x = self.gallery.thumbCount()
#         if x > 0:
#             self.UTILS.logComment("PLEASE VERIFY THE FOLLOWING " + str(x) + " IMAGES ....")
#             for i in range(0, x):
#                 # Click this thumbnail.
#                 self.gallery.clickThumb(i)
#                 
#                 # Take a screenshot (and update the comment).
#                 imgnam = self.UTILS.screenShot("14_" + str(i+1))
#                 self.UTILS.logComment("-> " + imgnam)
#                 
#                 # Check the size of the screenshot.
#                 # (because we can't guarentee the order, or match the filenames, we have to just loop through our
#                 # known sizes to see if this one's in there.
#                 img_size     = os.path.getsize(imgnam)
#                 size_matched = False
#                 for this_size in self._img_sizes:
#                     if img_size == this_size:
#                         size_matched = True
#                         break
#                         
#                 self.UTILS.TEST(size_matched,
#                     "Image size is as expected (it was " + str(self._img_sizes[i]) + " bytes). Please visually check the screenshots.")
#                 
#                 # Wait a second (or this test is done too quickly to see!)
#                 time.sleep(0.5)
#                 
#                 # Go back to the thumbnails.
#                 backBTN = self.UTILS.getElement(DOM.Gallery.fullscreen_back_button, "Back button")
#                 backBTN.tap()
#                 self.UTILS.waitForElements(DOM.Gallery.thumbnail_items, "Thumbnails")
        

