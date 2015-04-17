from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser


class test_main(PixiTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.browser = Browser(self)
        self.testURL = self.UTILS.general.get_config_variable("test_url", "common")

        self.UTILS.reporting.logComment("Using " + self.testURL)

        # switch off keyboard FTU screen
        self.data_layer.set_setting("keyboard.ftu.enabled", False)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Wifi needs to be off for this test to work.
        #
        self.data_layer.connect_to_cell_data()

        #
        # Open the browser app.
        #
        self.browser.launch()

        #
        # Open our URL.
        #
        self.browser.open_url(self.testURL)
