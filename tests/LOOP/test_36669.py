# Verify that the user can log-in into the app following the wizard
# (first time user uses the app) - Mobile ID

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
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.settings = Settings(self)

        self.connect_to_network()

        # Re-install Loop
        if self.loop.is_installed():
            self.loop.reinstall()
        else:
            self.loop.install()

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
            self.loop.phone_login()
            self.loop.allow_permission_phone_login()

            header = ('xpath', DOM.GLOBAL.app_head_specific.format("Firefox Hello"))
            self.UTILS.element.waitForElements(header, "Loop main view")