from OWDTestToolkit.pixi_testcase import PixiTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer

class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)


    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()

        self.dialer.enterNumber("123456789")

        self.dialer.createContactFromThisNum()

