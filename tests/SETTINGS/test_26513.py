#===============================================================================
# 26513: Data connection- Activation/Deactivation
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.network.disableAllNetworkSettings()

        self.UTILS.test.test(self.UTILS.network.is_network_type_enabled("data") == False, "Data conn is disabled.")

        self.settings.launch()
        self.settings.cellular_and_data()

        x = self.UTILS.element.getElement(DOM.Settings.celldata_DataConn_switch, "Data connection switch")
        x.tap()

        # Wait for confirmation screen
        self.settings.confirm_data_conn()

        self.UTILS.network.wait_for_network_item_enabled("data")

        self.UTILS.test.test(self.UTILS.network.is_network_type_enabled("data") == True, "Data conn is now enabled.")
