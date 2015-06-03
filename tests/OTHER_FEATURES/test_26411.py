
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser

class test_main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS     = UTILS(self)
        self.browser   = Browser(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.test.test(not self.UTILS.network.is_network_type_enabled("data"),
                         "Data mode is disabled before we start this test.")

        self.UTILS.statusbar.toggleViaStatusBar("data")
        self.wait_for_condition(lambda m: self.data_layer.is_cell_data_connected,
                                timeout=20, message="Device attached to data connection")

        self.browser.launch()
        self.browser.open_url("http://www.google.com")

        self.UTILS.statusbar.toggleViaStatusBar("data")
        self.wait_for_condition(lambda m: not self.data_layer.is_cell_data_connected,
                                timeout=20, message="Device attached to data connection")
        self.UTILS.element.waitForNotElements(DOM.Statusbar.dataConn, "Data icon in statusbar")

