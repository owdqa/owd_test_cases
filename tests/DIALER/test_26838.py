# 26838: Verify that the call log shows the ellipsis ("...") when contact
# has long names and that shows correctly the number of entries in call
# log groups

# ** Procedure
#       1. Make or receive more than one call to/from a contact with a long name
#       2. Go to the call log

# ** Expected Result
#       The call log entry must display the ellipsis (...) and the number of grouped calls.
#       EX: nameverylonghere... (2)

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer
import sys
sys.path.insert(1, "./")
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)

        self.test_num = ["666666666666", "555555555555"]
        self.test_contacts = [MockContact(tel={'type': 'Mobile',
                                                'value': self.test_num[i]}) for i in range(2)]

        self.test_contacts[0]["givenName"] = "LongGivennamexxxxxxxxxxx"
        self.test_contacts[1]["familyName"] = "LongFamilynamexxxxxxxxxxx"

        #
        # This has to be done due to a MockContact malfunction. It does not
        # update the name field to the specified values of givenName and familyName
        #
        for c in self.test_contacts:
            c["name"] = c["givenName"] + " " + c["familyName"]

        map(self.UTILS.general.insertContact, self.test_contacts)

        self.dialer.launch()
        self.dialer.callLog_clearAll()

        for contact in self.test_contacts:
            self.dialer.createMultipleCallLogEntries(contact["tel"]["value"], 2)
        self.dialer.openCallLog()

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):

        entries = self.UTILS.element.getElements(DOM.Dialer.call_log_numbers, "Call log entries", False)
        self.UTILS.reporting.logResult("info", "{} entries found.".format(len(entries)))

        for entry in entries:
            item = entry.find_element("xpath", "//span[@class='primary-info-main']")

            value = self.UTILS.element.get_css_value(item, "text-overflow")

            isEllipsis = self.UTILS.element.is_ellipsis_active(item)

            self.UTILS.reporting.logResult("info", "Value of css property: {}".format(value))
            self.UTILS.reporting.logResult("info", "isEllipsisActive? {}".format(isEllipsis))
            self.UTILS.test.TEST(
                value == "ellipsis" and isEllipsis, "Long entry in call log displays the ellipsis (...)")
