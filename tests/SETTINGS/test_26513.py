#===============================================================================
# 26513: Data connection- Activation/Deactivation
#===============================================================================

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
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.network.disableAllNetworkSettings()

        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("data") == False, "Data conn is disabled.")

        self.settings.launch()
        self.settings.cellular_and_data()

        x = self.UTILS.element.getElement(DOM.Settings.celldata_DataConn_switch, "Data connection switch")
        x.tap()

        #
        # Wait for confirmation screen
        #
        self.settings.confirm_data_conn()

        self.UTILS.network.waitForNetworkItemEnabled("data")

        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("data") == True, "Data conn is now enabled.")
