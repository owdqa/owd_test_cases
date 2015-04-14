# 27007: Call contact from overlay
#
# ** Prerrequesites
#       Address book has 3 contacts (A, B and C), the four digits typed matches as a substring of 
#       the 3 contacts phone number
# ** Procedure
#       1. Type 4 sequential  digits of contact A;
#       2. Tap on result count
#       3. Tap on a contact displayed
# ** Expected Results
#       1. In suggestion result count is 3 and result is first contact (in alphabetical order) 
#          of overlay menu;
#       2. Open the overlay menu and shows the three contacts in alphabetical order
#       3. Dial call to selected contact
#
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(FireCTestCase):

    def setUp(self):
        # Set up child objects...
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)

        self.names = ["Aname", "Bname", "Cname"]
        self.values = ["991234999", "999123499", "999912349"]
        self.test_contacts = [MockContact(givenName=self.names[i],
                                          tel=[{"type": "mobile", "value": self.values[i]}]) for i in range(3)]

        #
        # This has to be done due to a MockContact malfunction. It does not
        # update the name field to the specified values of givenName and familyName
        #
        for c in self.test_contacts:
            c["name"] = c["givenName"] + " " + c["familyName"]

        map(self.UTILS.general.insertContact, self.test_contacts)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()

        self.dialer.enterNumber("1234")

        suggestion_count_btn = self.UTILS.element.getElement(DOM.Dialer.suggestion_count, "Suggestion count")
        #
        # We are using this since normal .tap() method does not seem to be working
        #
        self.UTILS.element.simulateClick(suggestion_count_btn)

        self.UTILS.element.waitForElements(DOM.Dialer.suggestion_list, 'Suggestion list')
        items = self.UTILS.element.getElements(DOM.Dialer.suggestion_item_name, "Suggestion items", timeout=10)
        self.UTILS.test.test(len(items) == 3, "There are 3 contacts listed.")

        i = 0
        for c in self.test_contacts:
            self.UTILS.test.test(c["name"] in items[i].text,
                                 "The contact ({}) in suggestion list contains appears in suggestion list ({})"
                                 .format(c["name"], items[i].text))
            i += 1

        self.UTILS.reporting.logResult("info", "Tapping 1st contact listed ...")
        items[0].tap()

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)

        self.UTILS.element.waitForElements(("xpath", DOM.Dialer.outgoing_call_numberXP.format(self.test_contacts[0]["name"])),
                                           "Outgoing call found with number matching".format(self.test_contacts[0]["name"]))

        time.sleep(2)
        self.dialer.hangUp()
