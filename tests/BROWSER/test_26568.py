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

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):

        url1 = "www.google.com"
        url2 = "www.bbc.co.uk"

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
        self.browser.open_url(url1)
        self.browser.open_url(url2, timeout=60)  # bbc is heavier
