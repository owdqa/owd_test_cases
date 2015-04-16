# 26819: Delete entire call log when it has several calls, All tab
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer


class test_main(FireCTestCase):

    def setUp(self):
        # Set up child objects...
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.target_call_number = self.UTILS.general.get_config_variable("target_call_number", "common")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.createMultipleCallLogEntries(self.target_call_number, 4)
        self.dialer.callLog_clearAll()
