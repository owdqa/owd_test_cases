# OWD-36813
# Delete the NO revoked URL in Shared URL when there is only one Available entry - Clean Shared Links - Clean All

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.contacts import MockContact


class main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.settings = Settings(self)

        self.scenario = "scenarios/urls/single/available/idb"
        self.aux_files_dir = self.UTILS.general.get_config_variable("aux_files", "loop")
        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")
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

        self.loop.initial_test_checks()

        # Make sure we're not logged in FxA
        self.settings.launch()
        self.settings.fxa()
        self.settings.fxa_log_out()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.loop.launch()
        # This needs to be done at this point, bcs if the app is freshly installed the persistence
        # directories are not in its place until the app is launched for the first time
        self.loop.update_db("{}/{}".format(self.aux_files_dir, self.scenario))
        result = self.loop.wizard_or_login()

        if result:
            self.loop.firefox_login(self.fxa_user, self.fxa_pass)
            self.loop.allow_permission_ffox_login()
            self.UTILS.element.waitForElements(DOM.Loop.app_header, "Loop main view")

        self.loop.switch_to_urls()
        self.loop.open_settings()
        self.loop.delete_all_urls(cancel=False)

        self.UTILS.element.waitForElements(DOM.Loop.call_log, "Check we are returned to the call log")
        current = self.loop.get_number_of_available_urls()
        self.UTILS.test.test(current == 0, "Check that after deleting the URL, we have one less")
