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
        
        _url = "http://www.technicalinfo.net/papers/URLEmbeddedAttacks.html"
        
        #
        # Wifi needs to be off for this test to work.
        #
        self.UTILS.toggleViaStatusBar("data")
        
        #
        # Open the browser app.
        #
        self.Browser.launch()
        
        self.Browser.open_url(_url)
        x = self.Browser.loadedURL()
        self.UTILS.TEST(_url in x, "'%s' is in the loaded source url: '%s'." % (_url, x))
