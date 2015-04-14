#===============================================================================
# 26773: Verify that the user can uninstall a everything.me app through
# the grid edit mode
#
# Procedure:
# 1- open home screen
# 2- open edit mode
# 3- press X on app installed from everything.me
#
# Expected results:
# The user can uninstall a everything.me app through the grid edit mode
#===============================================================================

from OWDTestToolkit.firec_testcase import FireCTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
from marionette import Actions


class test_main(FireCTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.actions = Actions(self.marionette)
        self.settings = Settings(self)
        self.eme = EverythingMe(self)
        self.cat_id = "207"
        self.app_name = "Pacman"

        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
            self.apps.set_permission('Smart Collections', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("Unable to automatically set geolocation permission.")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()

        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        # First of all, make sure an application is installed
        self.eme.install_app(self.cat_id, self.app_name)
        self.UTILS.home.goHome()

        # Then, proceed to uninstall the application through the Edit mode
        self.UTILS.app.uninstallApp(self.app_name)
