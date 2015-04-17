from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact

class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)

        self.Contact_1 = MockContact(tel={'type': 'Mobile', 'value': '665666666'})
        self.num = self.Contact_1["tel"]["value"]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Enter a number in the dialer.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)

        self.dialer.call_this_number()

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of call being made:", x)

        self.dialer.hangUp()
