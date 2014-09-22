# OWD-35870
# Delete the revoked URL in Shared URL when there is only one revoked
# entry - Clean Shared Links - Clean Just disabled links

import sys
sys.path.insert(1, "./")
import os
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
from tests._mock_data.contacts import MockContact


class main(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)

        self.fxa_user = self.UTILS.general.get_os_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_os_variable("GLOBAL_FXA_PASS")

        # Insert our test contacts
        self.number_of_contacts = 3
        self.contact_given = "Test"
        self.contact_family = map(str, range(1, self.number_of_contacts + 1))
        self.contact_name = ["{} {}".format(self.contact_given, self.contact_family[i])
                             for i in range(self.number_of_contacts)]
        self.contact_numbers = ["666666666666", "777777777777", "649779117"]

        self.test_contacts = [MockContact(name=self.contact_name[i], givenName=self.contact_given,
                                          familyName=self.contact_family[i],
                                          tel={'type': 'Mobile', 'value': self.contact_numbers[i]})
                              for i in range(self.number_of_contacts)]
        map(self.UTILS.general.insertContact, self.test_contacts)

        # Directories
        self.persistent_directory = "/data/local/storage/persistent"
        loop_dir = os.popen("adb shell ls {} | grep loop".format(self.persistent_directory)).read().rstrip()
        target_dir = "{}/{}/idb/".format(self.persistent_directory, loop_dir)
        local_dir = "tests/LOOP/aux_files/scenarios/urls/single/revoked/idb"

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
        previous = self.loop.get_number_of_urls()

        self.loop.open_settings()
        self.loop.delete_just_revoked(cancel=False)

        self.UTILS.element.waitForElements(DOM.Loop.call_log, "Check we are returned to the call log")
        current = self.loop.get_number_of_urls()
        self.UTILS.test.TEST(
            previous - 1 == current, "Check that after deleting the URL, we have one less")
