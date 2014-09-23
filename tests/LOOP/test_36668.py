# Verify that the user can log-in into the app following the wizard
# (first time user uses the app) - Firefox Account

#
# DISCLAIMER
# This test needs a special build which includes our own version
# of the Market app so that we can upload apps that are not yet
# commercialy released (Like Firefox Hello). So you should re-flash
# the device before executing it.
#

import time
import os
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.browser import Browser
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.browser = Browser(self)
        self.settings = Settings(self)

        self.fxa_user = self.UTILS.general.get_os_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_os_variable("GLOBAL_FXA_PASS")
        self.market_url = "https://owd.tid.es/B3lg1r89n/market/appList.html"
        self.connect_to_network()

        # TODO - Uninstall & Install again Loop
        # Update loop
        result = os.popen("cd tests/LOOP/aux_files &&./publish_app.sh").read()
        chops = result.split("\n")
        self.UTILS.reporting.logResult('info', "result: {}".format(chops))
        self.UTILS.test.TEST("And all done, hopefully." in chops, "The script to publish an app is OK", True)

        # Re-install Loop
        self._reinstall_loop()

        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()

            header = ('xpath', DOM.GLOBAL.app_head_specific.format("Firefox Hello"))
            self.UTILS.element.waitForElements(header, "Loop main view")

    def _reinstall_loop(self):
        try:
            self.apps.uninstall(self.loop.app_name)
        except:
            self.UTILS.reporting.logResult('info', "App already uninstalled")

        self.wait_for_condition(lambda m: not self.apps.is_app_installed(
            self.loop.app_name), timeout=20, message="{} is not installed".format(self.loop.app_name))

        self.browser.launch()
        time.sleep(1)
        self.browser.open_url(self.market_url)

        loop_link = self.UTILS.element.getElement(
            ('xpath', '//p[contains(text(), "{}")]'.format(self.loop.app_name)), "App link")
        loop_link.tap()

        self.marionette.switch_to_frame()
        install_ok = self.UTILS.element.getElement(DOM.GLOBAL.app_install_ok, "Install button")
        install_ok.tap()

        msg = "{} installed".format(self.loop.app_name)
        installed_app_msg = (DOM.GLOBAL.system_banner_msg[0], DOM.GLOBAL.system_banner_msg[
                             1].format(msg))
        self.UTILS.element.waitForElements(installed_app_msg, "App installed", timeout=30)
