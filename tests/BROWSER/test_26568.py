#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils import UTILS
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
        self.UTILS.reportResults()

    def test_run(self):

        url1 = "www.google.com"
        url2 = "www.bbc.co.uk"

        #
        # Wifi needs to be off for this test to work.
        #
        self.UTILS.toggleViaStatusBar("data")

        #
        # Open the browser app.
        #
        self.Browser.launch()

        #
        # Open our URL.
        #
        self.Browser.open_url(url1)
        url = self.Browser.loadedURL()
        self.UTILS.TEST(url1 in url, "'{0}' is in the loaded source url: '{1}'.".format(url1, url))

        self.Browser.open_url(url2)
        url = self.Browser.loadedURL()
        self.UTILS.TEST(url2 in url, "'{0}' is in the loaded source url: '{1}'.".format(url2, url))
