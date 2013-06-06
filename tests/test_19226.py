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

class test_19226(GaiaTestCase):
    _Description = "[HOME SCREEN] Verify that when first launch a search-box is shown as well as a list of application categories."
    
    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        
        self.UTILS      = UTILS(self)
        self.EME        = EverythingMe(self)
        
        
        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        #
        # Launch the 'everything.me' app.
        #
        self.UTILS.logResult("info", "Launching EME ...")
        self.EME.launch()
        
        #
        # Verify that the search box is displayed, along with the
        # group categories.
        #
        self.UTILS.waitForElements(DOM.EME.groups, "Groups")
        self.UTILS.waitForElements(DOM.EME.search_field, "Search field")
