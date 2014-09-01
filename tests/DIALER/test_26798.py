# 26798: Make a call by typing a telephone number (mobile) which is not a contact. 
# Use country prefix (0034, 0039,+34)
# ** Procedure
#       1- Open dialer app
#       2- Write a number with prefix (0034, 0039,+34)
#       3- Make the call
# ** Expected Results
#       The call is successful
import time
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)

        #self.phone_number = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")
        self.contact_1 = MockContact()
        self.phone_number = self.contact_1["tel"]["value"]
        self.prefixes = ["0034", "0039", "+34"]
        self.test_numbers = [prefix + self.phone_number for prefix in self.prefixes]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def _do_the_call(self, number):
        self.dialer.enterNumber(number)
        self.dialer.call_this_number_and_hangup(5)
        # This needs to be done bcs sometimes (50%) the Dialer app crushes after hanging up
        self.apps.kill_all()
        time.sleep(2)
        self.dialer.launch()

    def test_run(self):
        #
        # Launch dialer app.
        #
        self.dialer.launch()
        map(self._do_the_call, self.test_numbers)