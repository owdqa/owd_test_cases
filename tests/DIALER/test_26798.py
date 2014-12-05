# 26798: Make a call by typing a telephone number (mobile) which is not a contact.
# Use country prefix (0034, 0039, +34)
# ** Procedure
#       1- Open dialer app
#       2- Write a number with prefix (0034, 0039, +34)
#       3- Make the call
# ** Expected Results
#       The call is successful
from gaiatest import GaiaTestCase
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer


class test_main(GaiaTestCase):

    def setUp(self):
        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)

        self.phone_number = self.UTILS.general.get_config_variable("target_call_number", "common")
        self.prefixes = ["0034", "+34"]
        self.test_numbers = [prefix + self.phone_number for prefix in self.prefixes]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def _do_the_call(self, number):
        self.dialer.enterNumber(number)
        self.dialer.call_this_number_and_hangup(5)

    def test_run(self):
        #
        # Launch dialer app.
        #
        self.dialer.launch()
        map(self._do_the_call, self.test_numbers)
