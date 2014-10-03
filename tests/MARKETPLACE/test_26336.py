#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.marketplace import Marketplace
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    APP_NAME = 'Wikipedia'
    APP_AUTHOR = 'tfinc'

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.Market = Marketplace(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        self.UTILS.reporting.logComment("Using app '" + self.APP_NAME + "'")

        #
        # Ensure we have a connection.
        #
        self.connect_to_network()

        #
        # Make sure our app isn't installed already.
        #
        self.UTILS.app.uninstallApp(self.APP_NAME)

        #
        # Launch market app.
        #
        self.Market.launch()

        #
        # Install our app.
        #
        self.UTILS.test.TEST(self.Market.installApp(self.APP_NAME, self.APP_AUTHOR),
                        "Successfully installed application '" + self.APP_NAME + "'.", True)

        #
        # Find the app icon on the homescreen.
        #
        self.UTILS.test.TEST(self.UTILS.findAppIcon(self.APP_NAME),
                        "Application '" + self.APP_NAME + "' is present on the homescreen.")
