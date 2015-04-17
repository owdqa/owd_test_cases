#===============================================================================
# 26761: Users can navigate to the landing page from the icongrid
#
# Pre-requisites:
# The phone is unlocked in the homescreen
#
# Procedure:
# 1-Do a swipe gesture to the left
#
# Expected results:
# The landing page is shown
#===============================================================================

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
import time


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)

        #
        # Don't prompt me for geolocation (this was broken recently in Gaia, so 'try' it).
        #
        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("Unable to automatically set Homescreen geolocation permission.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

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
        self.UTILS.element.waitForElements(("xpath", "//div[@id='icongrid']//div[@class='page'][2]"), "Icon page 2",
                                           True, 1, False)

        self.UTILS.home.scrollHomescreenLeft()
        time.sleep(1)
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Un-scrolling:", x)
        self.UTILS.element.waitForElements(("xpath", "//div[@id='icongrid']//div[@class='page'][1]"), "Icon page 1",
                                           True, 1, False)
        self.UTILS.element.waitForNotElements(("xpath", "//div[@id='icongrid']//div[@class='page'][2]"), "Icon page 2",
                                              True, 1, False)

        self.UTILS.home.scrollHomescreenLeft()
        time.sleep(1)
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Un-scrolling again (back to home page):", x)
        self.UTILS.element.waitForNotElements(("xpath", "//div[@id='icongrid']//div[@class='page'][1]"), "Icon page 1",
                                              True, 1, False)
        self.UTILS.element.waitForNotElements(("xpath", "//div[@id='icongrid']//div[@class='page'][2]"), "Icon page 2",
                                              True, 1, False)
