# OWD-34941:User must be prompted to log-ing into Loop, the first time the app is executed in the device.

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

        # Clean start
        if not self.loop.is_installed():
            self.loop.install()
        else:
            self.loop.reinstall()

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # First, login not finished
        self.loop.launch()
        self.loop.wizard_or_login()
        self.UTILS.element.waitForElements(DOM.Loop.wizard_login, "Login options prompted")
