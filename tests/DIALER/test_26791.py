#
# Imports which are standard for all test cases.
#
import sys
sys.path.insert(1, "./")
from gaiatest   import GaiaTestCase

#
# Imports particular to this test case.
#
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact


class test_main(GaiaTestCase):

    _testNum = "123456789"

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.Contact_1 = MockContact(tel={'type': 'Mobile', 'value': '111111111'})
        self.UTILS.general.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()

    def test_run(self):
        #
        # Enter a number in the dialer.
        #

        self.dialer.launch()
        self.dialer.enterNumber(self._testNum)

        #
        # Press the add to contacts button, then select 'add to existing contact'.
        #
        x = self.UTILS.element.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.add_to_existing_contact_btn, "Add to existing contact button")
        x.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.contacts.viewContact(self.Contact_1["name"], p_HeaderCheck=False)

        x = self.UTILS.element.getElement(("name", "tel[0][value]"), "Phone number 1")
        self.UTILS.test.TEST(x.get_attribute("value") == self.Contact_1["tel"]["value"],
                        "1st number is {} (it was {}).".format(self.Contact_1["tel"]["value"], x.get_attribute("value")))

        x = self.UTILS.element.getElement(("name", "tel[1][value]"), "Phone number 2")
        self.UTILS.test.TEST(x.get_attribute("value") == self._testNum,
                        "2nd number is {} (it was {}).".format(self._testNum, x.get_attribute("value")))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Final screenshot:", x)
