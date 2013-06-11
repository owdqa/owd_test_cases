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

class test_19253(GaiaTestCase):
    _Description = "(BLOCKED BY BUG 879816) [Gallery] Select multiple pictures and delete them."
    
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
            self.UTILS.addFileToDevice('./tests/resources/' + i, destination='DCIM/100MZLLA')
            
        #
        # Open the gallery application.
        #
        self.gallery.launch()
        
        #
        # Takes a few seconds for the thumbs to appear...
        #
        self.gallery.waitForThumbnails(len(self._img_list))
        
        #
        # Delete the first 3 thumbnails.
        #
        self.gallery.deleteThumbnails( (0,1,2) )
