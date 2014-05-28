#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)

        self.test_num = "666666666666"
        self.test_contacts = [MockContact(tel=[{'type': 'Mobile',
                         'value': self.test_num}]) for i in range(2)]

        self.test_contacts[0]["givenName"] = "LongGivennamexxxxxxxxxxx"
        self.test_contacts[1]["familyName"] = "LongFamilynamexxxxxxxxxxx"

        #
        # This has to be done due to a MockContact malfunction. It does not
        # update the name field to the specified values of givenName and familyName
        #
        for c in self.test_contacts:
            c["name"] = c["givenName"] + " " + c["familyName"]

        map(self.UTILS.general.insertContact, self.test_contacts)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        self.dialer.launch()
        self.dialer.callLog_clearAll()

        for contact in self.test_contacts:
            self.dialer.createMultipleCallLogEntries(contact["tel"][0]["value"], 1)

        entries = self.UTILS.element.getElements(DOM.Dialer.call_log_numbers, "Call log entries", False)
        self.UTILS.reporting.logResult("info", "{} entries found.".format(len(entries)))

        for element in entries:
            item = element.find_element("xpath", "//span[@class='primary-info-main']")

            value = self.UTILS.element.get_css_value(item, "text-overflow")
            isEllipsis = self.UTILS.element.is_ellipsis_active(item)

            self.UTILS.reporting.logResult("info", "Value of css property: {}".format(value))
            self.UTILS.reporting.logResult("info", "isEllipsisActive? {}".format(isEllipsis))
            self.UTILS.test.TEST(value == "ellipsis" and isEllipsis, "Value of css property")
