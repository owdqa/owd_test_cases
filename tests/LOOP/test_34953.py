# OWD-34953: Verify the user does not have the option to skip the sign-in
# dialog (e.g. he cannot access Loop Call Log or any other Loop screen).

# OWD-35813: Verify that loop user is logged-out from the app if I log-out my Firefox Account from Settings

from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.loop import Loop
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit import DOM


class main(FireCTestCase):

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.loop = Loop(self)
        self.settings = Settings(self)

        self.fxa_user = self.UTILS.general.get_config_variable("fxa_user", "common")
        self.fxa_pass = self.UTILS.general.get_config_variable("fxa_pass", "common")

        self.data_layer.connect_to_wifi()

        self.loop.initial_test_checks()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        # First, login
        self.loop.launch()
        result = self.loop.wizard_or_login()

        if result:
            self.UTILS.element.waitForElements(DOM.Loop.wizard_login, "Loop login")
            self.UTILS.element.waitForNotElements(DOM.Loop.app_header, "Loop main view")
            self.UTILS.element.waitForNotElements(DOM.Loop.settings_panel, "Settings panel")
            self.UTILS.element.waitForNotElements(DOM.Loop.calls_section, "Call log")
            self.UTILS.element.waitForNotElements(DOM.Loop.shared_links_section, "Urls section")
