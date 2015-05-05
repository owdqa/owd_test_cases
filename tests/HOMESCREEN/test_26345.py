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
import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class test_main(SpreadtrumTestCase):

    test_url = "http://everlong.org/mozilla/packaged/"
    _appName = "cool packaged app"
    _appOK = True
    install_button_locator = ('id', 'install-app')
    confirm_install_locator = ('id', 'app-install-install-button')

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.settings = Settings(self)
        self.browser = Browser(self)

        self.connect_to_network()
        # Uninstall the app (if need be).
        self.UTILS.app.uninstallApp(self._appName)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.browser.launch()
        self.browser.open_url(self.test_url)
        """
        Install the app (these DOM items are peculiar to this little dev app,
        so dont bother putting them in the main DOM.py file).
        """
        install_btn = self.UTILS.element.getElement(self.install_button_locator, "Install an app button")
        install_btn.tap()

        # Install button on the splash screen (switch to main frame to 'see' this).
        self.marionette.switch_to_frame()
        install_btn = self.UTILS.element.getElement(self.confirm_install_locator, "Install button", True, 30)
        install_btn.tap()

        ok_btn = self.UTILS.element.getElement(DOM.GLOBAL.modal_dialog_alert_ok, "Ok button")
        ok_btn.tap()

        expected_msg = "{} installed".format(self._appName)
        system_banner = self.UTILS.element.getElement(DOM.GLOBAL.system_banner, "System notification banner")
        self.UTILS.test.test(system_banner.text == expected_msg, "Banner matches expected message")
        self.apps.kill_all()
        time.sleep(2)

        # Go back to the home page and check the app is installed.
        self.UTILS.test.test(self.UTILS.app.launchAppViaHomescreen(self._appName),
                             "Application '" + self._appName + "' can be launched from the homescreen.", True)
