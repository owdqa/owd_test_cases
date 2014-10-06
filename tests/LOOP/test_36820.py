# OWD - 36820
# Delete the NO revoked URL in Shared URL when there are NO revoked
# entries in different days - Clean Shared Links - Clean Just Disabled
# links

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
        self.settings = Settings(self)

        self.scenario = "scenarios/urls/multiple/available/diff_day/idb"
        self.aux_files_dir = self.UTILS.general.get_os_variable("GLOBAL_LOOP_AUX_FILES")
        self.fxa_user = self.UTILS.general.get_os_variable("GLOBAL_FXA_USER")
        self.fxa_pass = self.UTILS.general.get_os_variable("GLOBAL_FXA_PASS")
        self.connect_to_network()

        # Insert our test contacts
        number_of_contacts = 3
        contact_given = "Test"
        contact_family = map(str, range(1, number_of_contacts + 1))
        contact_name = ["{} {}".format(contact_given, contact_family[i])
                        for i in range(number_of_contacts)]
        contact_numbers = ["666666666666", "777777777777", "888888888888"]

        test_contacts = [MockContact(name=contact_name[i], givenName=contact_given,
                                     familyName=contact_family[i],
                                     tel={'type': 'Mobile', 'value': contact_numbers[i]})
                         for i in range(number_of_contacts)]
        map(self.UTILS.general.insertContact, test_contacts)

        # Re-install Loop
        if self.loop.is_installed():
            self.loop.reinstall()
        else:
            self.loop.install()

        # Make sure we're not logged in FxA
        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.loop.launch()
        # This needs to be done at this point, bcs if the app is freshly installed the persistence
        # directories are not in its place until the app is launched for the first time
        self.loop.update_db("{}/{}".format(self.aux_files_dir, self.scenario))
        result = self.loop.wizard_or_login()

        if result:
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()

        header = ('xpath', DOM.GLOBAL.app_head_specific.format("Firefox Hello"))
        self.UTILS.element.waitForElements(header, "Loop main view")

        self.loop.switch_to_urls()
        previous = self.loop.get_number_of_available_urls()

        self.loop.open_settings()
        self.loop.delete_just_revoked(cancel=False)

        self.UTILS.element.waitForElements(DOM.Loop.call_log, "Check we are returned to the call log")
        current = self.loop.get_number_of_available_urls()
        self.UTILS.test.TEST(
            previous == current,
            "Check that after deleting the revoked of different days when there are none, nothing has changed")