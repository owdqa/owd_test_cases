#===============================================================================
# 26345: Launch a packaged app - verify the app launches successfully to the
# correct content
#
# Procedure:
# 1- Open settings app
# 2- Select Cellular and Data option
# 3- Activate Data connection
# ER1
# 4- Open Marketplace app
# 5- Search "Privilege App Testing"
# 6- Press install app button
# 7- Press install button
# ER2
# 8- Try to open the installed packaged app
# ER3
#
# Expected results:
# ER1 Data connection is activated
# ER2 The app is installed with the correct icon
# ER3 The app is launched correctly
#===============================================================================

from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class test_main(GaiaTestCase):

    _URL = "http://everlong.org/mozilla/packaged/"
    _appName = "cool packaged app"
    _appOK = True

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.Browser = Browser(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        #
        # Ensure we have a connection.
        #
        self.connect_to_network()

        #
        # Uninstall the app (if need be).
        #
        self.UTILS.app.uninstallApp(self._appName)

        #
        # Open the browser app.
        #
        self.Browser.launch()

        #
        # Open our URL.
        #
        self.Browser.open_url(self._URL)

        #
        # Install the app (these DOM items are peculiar to this little dev app,
        # so dont bother putting them in the main DOM.py file).
        #
        x = ('id', 'install-app')
        install_btn = self.UTILS.element.getElement(x, "Install an app button")
        install_btn.tap()

        # Install button on the splash screen (switch to main frame to 'see' this).
        self.marionette.switch_to_frame()

        x = ('id', 'app-install-install-button')
        install_btn = self.UTILS.element.getElement(x, "Install button")
        install_btn.tap()

        # ... and switch back to brwoser to see the next splash screen(!)
        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)
        btn = self.UTILS.element.getElement(DOM.GLOBAL.modal_alert_ok, "Ok button")
        btn.tap()

        #
        # Go back to the home page and check the app is installed.
        #
        self.UTILS.test.test(self.UTILS.app.launchAppViaHomescreen(self._appName),
                        "Application '" + self._appName + "' can be launched from the homescreen.", True)
