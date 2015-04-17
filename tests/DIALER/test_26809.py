from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
import time

class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        #
        # Enter a number in the dialer.
        #
        self.dialer.launch()


        self.dialer.open_call_log()

        time.sleep(2)
        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of call log:", x)
