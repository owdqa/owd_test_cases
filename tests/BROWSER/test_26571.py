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
        
        self.test_url = "http://www.technicalinfo.net/papers/URLEmbeddedAttacks.html"

        #
        # Get some connection, no matter which (wifi, data)
        #
        self.connect_to_network()

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Open the browser app.
        #
        self.browser.launch()

        self.browser.open_url(self.test_url)
        loaded_url = self.browser.loadedURL()
        self.UTILS.test.TEST(self.test_url in loaded_url, "'{0}' is in the loaded source url: '{1}'."
                        .format(self.test_url, loaded_url))
