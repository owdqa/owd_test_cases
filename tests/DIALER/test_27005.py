# 27005: Three matches at 4th digit
#
# ** Prerrequisites
#       Address book has 3 contacts (A, B and C); the four digits typed matches as a substring of the three
#       contacts phone number (e.g.6869 matches 686974951 and 666686986)
# ** Procedure
#       1. Type three sequential digits of phone number of contact A (B & C);
#       2. Type 4th digit of phone number of contact A  (B & C);
#       3. Tap on result count;
#       4. Tap on cancel
#
# ** Expected Results
#
#       1. Suggestion remain empty;
#       2. In suggestion result count is 3 and result is first contact (in alphabetically order) of overlay menu;
#       3. Overlay menu appears showing the 3 contacts; verify they are alphabetically ordered;
#       4. Overlay menu is closed

import time
from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


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

        # This has to be done due to a MockContact malfunction. It does not
        # update the name field to the specified values of givenName and familyName
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

        # We are using this since normal .tap() method does not seem to be working
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

        x = self.UTILS.element.getElement(DOM.Dialer.suggestion_list_cancel, "Cancel button")
        x.tap()

        suggestion_overlay = self.UTILS.element.getElement(DOM.Dialer.suggestion_overlay, "Suggestion overlay")
        self.UTILS.test.test(suggestion_overlay.get_attribute("aria-hidden"), "Overlay is hidden after tapping on cancel button")