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
        
        #
        # Don't prompt me for geolocation (this was broken recently in Gaia, so 'try' it).
        #
        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        except:
            self.UTILS.logComment("(Just FYI) Unable to automatically set Homescreen geolocation permission.")

        
    def tearDown(self):
        self.UTILS.reportResults()
        
    def test_run(self):
        
        self.UTILS.goHome()

        self.UTILS.scrollHomescreenRight()
        time.sleep(1)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Scrolling left:", x)
        self.UTILS.waitForElements(("xpath", "//div[@id='icongrid']//div[@class='page'][1]"), "Icon page 1", True, 1, False)
        
        self.UTILS.scrollHomescreenRight()
        time.sleep(1)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Scrolling left again:", x)
        self.UTILS.waitForElements(("xpath", "//div[@id='icongrid']//div[@class='page'][2]"), "Icon page 2", True, 1, False)
        
        self.UTILS.scrollHomescreenLeft()
        time.sleep(1)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Un-scrolling:", x)
        self.UTILS.waitForElements(("xpath", "//div[@id='icongrid']//div[@class='page'][1]"), "Icon page 1", True, 1, False)
        self.UTILS.waitForNotElements(("xpath", "//div[@id='icongrid']//div[@class='page'][2]"), "Icon page 2", True, 1, False)
        
        self.UTILS.scrollHomescreenLeft()
        time.sleep(1)
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Un-scrolling again (back to home page):", x)
        self.UTILS.waitForNotElements(("xpath", "//div[@id='icongrid']//div[@class='page'][1]"), "Icon page 1", True, 1, False)
        self.UTILS.waitForNotElements(("xpath", "//div[@id='icongrid']//div[@class='page'][2]"), "Icon page 2", True, 1, False)
        
