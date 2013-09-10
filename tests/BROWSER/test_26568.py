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
        self.Browser    = Browser(self)
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        _url1 = "www.google.com"
        _url2 = "www.bbc.co.uk"
        
        #
        # Wifi needs to be off for this test to work.
        #
        self.UTILS.toggleViaStatusBar("data")
        
        #
        # Open the browser app.
        #
        self.Browser.launch()
        
        #
        # Open our URL.
        #
        self.Browser.open_url(_url1)
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        _url = self.Browser.loadedURL()
        self.UTILS.TEST(_url1 in _url, "'%s' is in the loaded source url: '%s'." % (_url1, _url))

        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        
        self.Browser.open_url(_url2)
        _url = self.Browser.loadedURL()
        self.UTILS.TEST(_url2 in _url, "'%s' is in the loaded source url: '%s'." % (_url2, _url))
        

        
        