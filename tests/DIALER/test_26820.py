# 26820: Delete some entries from the call log when it has several calls, All tab
# ** Procedure
#       1-Open call log, Missed calls tab
#       2-Enter edit mode
#       3-Select 2 or 3 calls
#       4-Press the button Delete
# ** Expected Results
#       The entries selected are deleted from the call log.
# TODO: Review this test

from OWDTestToolkit.pixi_testcase import PixiTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer
import time


class test_main(PixiTestCase):

    def setUp(self):
        # Set up child objects...
        PixiTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        PixiTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()

        self.dialer.createMultipleCallLogEntries(self.UTILS.general.get_config_variable("target_call_number", "common"), 3)

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of multiple entries:", screenshot)

        self.dialer.callLog_clearSome([1, 2])
        time.sleep(5)

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of some entries removed:", screenshot)
