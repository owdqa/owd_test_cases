#===============================================================================
# 26513: Data connection- Activation/Deactivation
#===============================================================================

import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def __init__(self, *args, **kwargs):
        kwargs['restart'] = True
        super(test_main, self).__init__(*args, **kwargs)
        
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
        time.sleep(1)
        self.settings.cellular_and_data()

        data_switch = self.UTILS.element.getElement(DOM.Settings.celldata_DataConn_switch, "Data connection switch")
        data_switch.tap()

        # Wait for confirmation screen
        self.settings.confirm_data_conn()

        self.UTILS.network.wait_for_network_item_enabled("data")

        self.UTILS.test.test(self.UTILS.network.is_network_type_enabled("data") == True, "Data conn is now enabled.")
