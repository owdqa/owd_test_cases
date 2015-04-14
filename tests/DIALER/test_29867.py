import time
import sys
sys.path.insert(1, "./")
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.settings import Settings
from OWDTestToolkit.apps.dialer import Dialer
from tests.i18nsetup import setup_translations


class test_main(FireCTestCase):

    def setUp(self):
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.settings = Settings(self)
        _ = setup_translations(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        # Launch dialer app.
        self.dialer.launch()
        self.dialer.enterNumber("#31#")

        # Calls the current number.
        call_button = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call number button")
        call_button.tap()

        msg = self.UTILS.element.getElement(DOM.Dialer.message_callerID, "Message Call ID")
        self.UTILS.test.test(msg.text == _("Service has been disabled"), "Caller ID NOT restricted")
