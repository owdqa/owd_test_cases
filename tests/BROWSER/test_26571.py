#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.browser = Browser(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        test_url = "http://www.technicalinfo.net/papers/URLEmbeddedAttacks.html"

        #
        # Wifi needs to be off for this test to work.
        #
        self.data_layer.connect_to_cell_data()
        #
        # Open the browser app.
        #
        self.browser.launch()

        self.browser.open_url(test_url)
        loaded_url = self.browser.loadedURL()
        self.UTILS.test.TEST(test_url in loaded_url, "'{0}' is in the loaded source url: '{1}'."
                        .format(test_url, loaded_url))
