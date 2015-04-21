
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser


class test_main(PixiTestCase):

    def setUp(self):
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.browser = Browser(self)
        self.data_layer.set_setting('ril.data.enabled', False)
        self.UTILS.app.setPermission('Browser', 'geolocation', 'deny')

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

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
                                timeout=40, message="Device attached to data connection")
        self.UTILS.element.waitForNotElements(DOM.Statusbar.dataConn, "Data icon in statusbar")
