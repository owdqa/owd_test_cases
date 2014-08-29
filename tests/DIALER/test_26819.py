# 26819: Delete entire call log when it has several calls, All tab
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 4)
        self.dialer.callLog_clearAll()
