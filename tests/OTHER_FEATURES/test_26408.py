
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS


class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.test.TEST(not self.UTILS.network.is_network_type_enabled("airplane"),
                             "Airplane mode is disabled before we start this test.")

        self.UTILS.statusbar.toggleViaStatusBar("airplane")
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForElements(DOM.Statusbar.airplane, "Airplane icon in statusbar", True, 20, True)

        self.UTILS.statusbar.toggleViaStatusBar("airplane")
        self.UTILS.element.waitForNotElements(DOM.Statusbar.airplane, "Airplane icon in statusbar")
