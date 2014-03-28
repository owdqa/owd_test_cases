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
        
        x = self.UTILS.element.getElement(DOM.Settings.celldata_DataConn_switch, "Data connection switch")
        x.tap()

        #
        # Wait for confirmation screen
        #
        try:
            self.wait_for_element_displayed(*DOM.Settings.celldata_DataConn_ON, timeout=10)
            x = self.marionette.find_element(*DOM.Settings.celldata_DataConn_ON)
            if x.is_displayed():
                x.tap()
        except: #element present but not displayed
            #
            # If we arrive here, that means the confirmation screen is not shown, because
            # it was already accepted some time before
            #
            # What does it mean such a thing? It means that we now have data connection,
            # so nothing else is required
            pass

        self.UTILS.network.waitForNetworkItemEnabled("data")

        self.UTILS.test.TEST(self.UTILS.network.isNetworkTypeEnabled("data") == True, "Data conn is now enabled.")
