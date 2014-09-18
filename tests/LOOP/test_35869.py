# 35869: Cancel the action of deleting an entry in the Shared URL - Setting Option

import os
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit import DOM


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.persistent_directory = "/data/local/storage/persistent"
    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        a_try = os.popen("adb shell ls {} | grep loop".format(self.persistent_directory)).read()
        target_dir = "{}/{}/idb/".format(self.persistent_directory, a_try)
        self.UTILS.reporting.logResult('info', "Directory: {}".format(target_dir))

        os.system("cd tests/LOOP/aux_files/idb && adb push . {}".format(target_dir))