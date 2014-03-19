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
        self.Browser = Browser(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        test_url = "http://www.technicalinfo.net/papers/URLEmbeddedAttacks.html"

        #
        # Wifi needs to be off for this test to work.
        #
        self.UTILS.statusbar.toggleViaStatusBar("data")

        #
        # Open the browser app.
        #
        self.Browser.launch()

        self.Browser.open_url(test_url)
        loaded_url = self.Browser.loadedURL()
        self.UTILS.test.TEST(test_url in loaded_url, "'{0}' is in the loaded source url: '{1}'."
                        .format(test_url, loaded_url))
