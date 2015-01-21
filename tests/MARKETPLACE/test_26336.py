#===============================================================================
# 26336: Install a market installed hosted app - verify the app is installed with
# the right icon
#
# Procedure:
# 1- Open marketplace app
# 2- Select an app
# 3- Press install button
#
# Expected results:
# The app is installed with the right icon
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.marketplace import Marketplace
from OWDTestToolkit.apps.settings import Settings


class test_main(GaiaTestCase):

    APP_NAME = 'Wikipedia'
    APP_AUTHOR = 'Wikimedia Foundation'

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.market = Marketplace(self)
        self.settings = Settings(self)
        self.connect_to_network()
        # Make sure our app isn't installed already.
        self.UTILS.app.uninstallApp(self.APP_NAME)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.market.launch()
        # Install our app.
        self.UTILS.test.test(self.market.install_app(self.APP_NAME, self.APP_AUTHOR),
                             "Successfully installed application '" + self.APP_NAME + "'.", True)
        # Find the app icon on the homescreen.
        self.UTILS.test.test(self.UTILS.app.findAppIcon(self.APP_NAME),
                             "Application '" + self.APP_NAME + "' is present on the homescreen.")
