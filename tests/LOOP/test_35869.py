# 35869
# Cancel the action of deleting an entry in the Shared URL - Setting Option

import os
import time
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

        self.fxa_user = self.UTILS.general.get_os_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_os_variable("GLOBAL_FXA_PASS")

        # Directories
        self.persistent_directory = "/data/local/storage/persistent"
        loop_dir = os.popen("adb shell ls {} | grep loop".format(self.persistent_directory)).read().rstrip()
        target_dir = "{}/{}/idb/".format(self.persistent_directory, loop_dir)
        local_dir = "tests/LOOP/aux_files/scenarios/urls/multiple/available/same_day/idb"

        # Prepopulate urls
        os.system("cd {} && adb push . {}".format(local_dir, target_dir))

        self.connect_to_network()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()

        header = ('xpath', DOM.GLOBAL.app_head_specific.format("Firefox Hello"))
        self.UTILS.element.waitForElements(header, "Loop main view")
        self.loop.switch_to_urls()