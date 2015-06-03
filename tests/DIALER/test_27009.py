from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
import time

class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)

        self.cont1 = MockContact(tel=[{"type": "Mobile", "value": "111111111"}])
        self.UTILS.general.insertContact(self.cont1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.enterNumber("123")
        time.sleep(1)

        self.UTILS.element.waitForNotElements(DOM.Dialer.suggestion_count, "Suggestion count")
        self.UTILS.element.waitForNotElements(DOM.Dialer.suggestion_item, "Suggestion item")

        self.dialer.enterNumber("4")
        time.sleep(1)

        self.UTILS.element.waitForNotElements(DOM.Dialer.suggestion_count, "Suggestion count")
        self.UTILS.element.waitForNotElements(DOM.Dialer.suggestion_item, "Suggestion item")
