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
import time

class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)

        self.names = ["Aname", "Bname", "Cname"]
        self.values = ["991234999", "999123499", "999912349"]
        self.test_contacts = [MockContact(givenName=self.names[i],
            tel=[{"type":"mobile", "value": self.values[i]}]) for i in range(3)]

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
        self.dialer.enterNumber("1234")

        x = self.UTILS.element.getElement(DOM.Dialer.suggestion_count, "Suggestion count")
        #
        # We are using this since normal .tap() method does not seem to be working
        #
        self.UTILS.element.simulateClick(x)

        x = self.UTILS.element.getElements(DOM.Dialer.suggestion_list, "Suggestion list")
        self.UTILS.test.TEST(len(x) == 3, "There are 3 contacts listed.")

        i = 0
        for c in self.test_contacts:
            self.UTILS.test.TEST(c["name"] in x[i].text,
                    "The first contact listed contains '{}' (it was '{}')".format(c["name"], x[i].text))
            i += 1

        self.UTILS.reporting.logResult("info", "Tapping 1st contact listed ...")
        x[0].tap()

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)

        self.UTILS.element.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP.format(self.test_contacts[0]["name"])),
                                    "Outgoing call found with number matching".format(self.test_contacts[0]["name"]))

        time.sleep(2)
        self.dialer.hangUp()