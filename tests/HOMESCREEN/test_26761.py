#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit.utils.utils import UTILS
import time


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
            self.UTILS.reporting.logComment("(Just FYI) Unable to automatically set Homescreen geolocation permission.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        self.UTILS.home.goHome()

        self.UTILS.home.scrollHomescreenRight()
        time.sleep(1)
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Scrolling left:", x)
        self.UTILS.element.waitForElements(("xpath", "//div[@id='icongrid']//div[@class='page'][1]"), "Icon page 1",
                                           True, 1, False)

        self.UTILS.home.scrollHomescreenRight()
        time.sleep(1)
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Scrolling left again:", x)
        self.UTILS.element.waitForElements(("xpath", "//div[@id='icongrid']//div[@class='page'][2]"), "Icon page 2", True, 1, False)

        self.UTILS.home.scrollHomescreenLeft()
        time.sleep(1)
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Un-scrolling:", x)
        self.UTILS.element.waitForElements(("xpath", "//div[@id='icongrid']//div[@class='page'][1]"), "Icon page 1", True, 1, False)
        self.UTILS.element.waitForNotElements(("xpath", "//div[@id='icongrid']//div[@class='page'][2]"), "Icon page 2", True, 1, False)

        self.UTILS.home.scrollHomescreenLeft()
        time.sleep(1)
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Un-scrolling again (back to home page):", x)
        self.UTILS.element.waitForNotElements(("xpath", "//div[@id='icongrid']//div[@class='page'][1]"), "Icon page 1", True, 1, False)
        self.UTILS.element.waitForNotElements(("xpath", "//div[@id='icongrid']//div[@class='page'][2]"), "Icon page 2", True, 1, False)

