#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.UTILS.network.disableAllNetworkSettings()

        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("data") == False, "Data conn is disabled.")

        self.settings.launch()
        self.settings.cellular_and_data()
        x = self.UTILS.element.getElement(("xpath", "//a[text()='Data connection']"), "Data connection switch")
        x.tap()
        self.wait_for_element_displayed(*DOM.settings.celldata_DataConn_ON, timeout=10)
        x = self.marionette.find_element(*DOM.settings.celldata_DataConn_ON)
        if x.is_displayed():
            x.tap()

        self.UTILS.network.waitForNetworkItemEnabled("data")

        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("data") == True, "Data conn is now enabled.")
