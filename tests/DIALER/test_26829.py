# 26829: Verify that If the call log is empty, edit button is disabled
# **Procedure
#   Open call log (call log is empty)
# **ER
#   Edit button is disabled
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.callLog_clearAll()

        self.dialer.openCallLog()

        x = self.UTILS.element.getElement(DOM.Dialer.call_log_edit_btn, "Edit button", False)
        #Try with attribute aria-disabled
        self.UTILS.test.test(x.get_attribute("aria-disabled"), "The edit button is disabled.") 
