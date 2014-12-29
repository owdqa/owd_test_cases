# 27022: Call the number
# ** Procedure
#       1. Open call log
#       2. Tap on Unknown number
# ** Expected Results
#       1. An entry with call to a number with unknown name is displayed
#       2. A call to number is started
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)

        self.phone_number = self.UTILS.general.get_config_variable("target_call_number", "common")
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.phone_number, 1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        # Open the call log and tap on the phone_number.
        self.dialer.open_call_log()
        self.dialer.callLog_call(self.phone_number)
        time.sleep(3)
        self.dialer.hangUp()
