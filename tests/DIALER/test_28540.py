# 28540: Press call button while the call log contains different outgoing calls
#
# ** Procedure
#       1. Open dialer app
#       2. Press call button
# ** Expected result
#       Tapping on the Call button retrieves the most recent outgoing number from the call log

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):

        #
        # Set up child objects...
        #
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        self.test_contacts = [MockContact() for i in range(3)]
        self.test_numbers = [self.test_contacts[i]["tel"]["value"] for i in range(len(self.test_contacts))]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()

        # Delete all call log
        self.dialer.callLog_clearAll()

        # Call each number
        map(self._do_the_call, self.test_numbers)

        # Tapping call button
        x = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call button")
        x.tap()

        # Make sure that after tapping, we get the last outgoing call in the call log
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        self.UTILS.reporting.logResult('info', "Dialer num: {}".format(dialer_num))
        self.UTILS.test.TEST(str(self.test_contacts[-1]["tel"]["value"]) == dialer_num,
                             "After calling several contacts, if we press 'Call' button, we get the last one's phone_number")

        y = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screen shot of the result of tapping call button", y)

    def _do_the_call(self, number):
        self.dialer.enterNumber(number, validate=False)
        self.dialer.call_this_number_and_hangup(5)
