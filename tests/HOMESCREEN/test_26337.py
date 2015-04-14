#===============================================================================
# 26337: Launch market installed hosted app - verify the app is launched
# successfully from the homescreen
#
# Procedure:
# 1- Open marketplace app
# 2- Select an app
# 3- Press install button
# ER1
# 4- Open the installed app
# ER2
#
# Expected results:
# ER1 The app is installed with the right icon
# ER2 The app is launched successfully
#===============================================================================

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.marketplace import Marketplace
from OWDTestToolkit.apps.settings import Settings


class test_main(FireCTestCase):

    APP_NAME = 'Wikipedia'
    APP_AUTHOR = 'Wikimedia Foundation'

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.market = Marketplace(self)
        self.settings = Settings(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):

        self.UTILS.reporting.logComment("Using app '" + self.APP_NAME + "'")

        #
        # Ensure we have a connection.
        #
        self.data_layer.connect_to_wifi()

        #
        # Make sure our app isn't installed already.
        #
        self.UTILS.app.uninstallApp(self.APP_NAME)

        #
        # Launch market app.
        #
        self.market.launch()

        #
        # Install our app.
        #
        self.UTILS.test.test(self.market.install_app(self.APP_NAME, self.APP_AUTHOR),
                        "Successfully installed application '" + self.APP_NAME + "'.", True)

        #
        # Launch the app from the homescreen.
        #
        self.UTILS.test.test(self.UTILS.app.launchAppViaHomescreen(self.APP_NAME),
                        "Application '" + self.APP_NAME + "' can be launched from homescreen.")
