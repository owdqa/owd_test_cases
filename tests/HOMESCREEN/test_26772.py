#===============================================================================
# 26772: Verify that if the user tries to install an already installed
# application,she is notified about it
#
# Procedure:
# 1- Open everything.me
# 2- Search by text to found a app which had been already installed
# 3- Do a long-tap on this app
#
# Expected result:
# If the user tries to install an application already installed, he is
# notified about it
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.everythingme import EverythingMe
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
from marionette import Actions
import time


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)

        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.eme = EverythingMe(self)
        self.actions = Actions(self.marionette)
        self.cat_id = "207"
        self.app_name = "Pacman"

        try:
            self.apps.set_permission('Homescreen', 'geolocation', 'deny')
            self.apps.set_permission('Smart Collections', 'geolocation', 'deny')
        except:
            self.UTILS.reporting.logComment("Unable to automatically set geolocation permission.")

        # Try to uninstall app, just in case it was previously installed
        self.UTILS.app.uninstallApp(self.app_name)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.data_layer.connect_to_wifi()

        self.UTILS.iframe.switchToFrame(*DOM.Home.frame_locator)

        # First of all, make sure an application is installed
        installed = self.eme.install_app(self.cat_id, self.app_name)
        self.UTILS.test.TEST(installed, "The application {} was successfully installed".format(self.app_name))

        # Go back and try to reinstall again
        self.UTILS.home.goHome()
        installed = self.eme.install_app(self.cat_id, self.app_name, False)
        self.UTILS.test.TEST(not installed, "The application {} was already previously installed".\
                                            format(self.app_name))

        self.UTILS.app.uninstallApp(self.app_name)
