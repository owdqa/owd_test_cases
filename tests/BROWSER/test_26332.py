#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.browser = Browser(self)

        self.testURL = self.UTILS.general.get_os_variable("GLOBAL_TEST_URL")

        #
        # Get Wifi
        #
        self.data_layer.connect_to_wifi()

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Open the browser app.
        #
        self.browser.launch()

        #
        # Open our URL.
        #
        self.browser.open_url(self.testURL)
