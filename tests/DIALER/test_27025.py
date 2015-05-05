# 27025: Call log in edit mode
# ** Procedure
#       1. Open call log
#       2. Tap on edit option
#       3. Tap on any entry not saved as a contact

# ** Expected Results
#       1. An entry with call from a number with unknown name is displayed
#       2. Call log is editable
#       3. Nothing should happen

import time
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer


class test_main(SpreadtrumTestCase):

    def setUp(self):
        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")

        # Create a call log entry
        self.dialer.launch()
        self.dialer.callLog_clearAll()
    
        self.dialer.createMultipleCallLogEntries(self.phone_number, 2)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Open the call log and select Add to Contact.
        self.dialer.open_call_log()

        edit_btn = self.UTILS.element.getElement(DOM.Dialer.call_log_edit_btn, "Edit button")
        edit_btn.tap()

        # Now tap the number and verify that we're not taken to the menu,
        entry = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(self.phone_number)),
                                              "The call log for number {}".format(self.phone_number))
        entry.tap()

        self.UTILS.reporting.logResult("info", "Checking that the call to [{}] is not set up".
                                       format(self.phone_number))
        self.apps.switch_to_displayed_app()
        self.UTILS.element.waitForNotElements(DOM.Dialer.hangup_bar_locator, "Not calling in edit mode", timeout=10)
