# 26819: Delete entire call log when it has several calls, All tab
from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer


class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 4)
        self.dialer.callLog_clearAll()
