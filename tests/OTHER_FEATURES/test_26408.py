#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS



class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        #
        # Data conn icon is not in status bar yet.
        #
        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("airplane") == False,
                         "Airplane mode is disabled before we start this test.")

        #
        # Enable airplane mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar("airplane")

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForElements(DOM.Statusbar.airplane, "Airplane icon in statusbar", True, 20, False)

        #
        # Disable airplane mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar("airplane")

        #
        # Data icon is no longer visible in status bar.
        #
        self.UTILS.element.waitForNotElements(DOM.Statusbar.airplane, "Airplane icon in statusbar")

