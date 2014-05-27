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

        self.urls = ["www.google.com", "www.bbc.co.uk"]
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

        #
        # Check we can go from a site to another
        #
        map(self.do_open_url, self.urls)

    def do_open_url(self, url):
        #
        # Open our URL.
        #
        self.browser.open_url(url)
        loaded_url = self.browser.loadedURL()
        self.UTILS.test.TEST(url in loaded_url, "'{0}' is in the loaded source url: '{1}'.".format(url, loaded_url))
