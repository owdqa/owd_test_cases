#27010: Start dialing a number which match with one contact's number with prefix
#
# ** Pre-requisites
#   Address book has at least one contact  stored with prefix and with the four digits dialed 
#   that matches as a substring of the contact phone number, i.e +34 657 890
# ** Procedure
#   1. Type four digits of contacts phone numbers,  i.e  7890
# ** Expected Results
#   1. The contact which matches is shown
#   
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):
        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.test_contacts = [MockContact() for i in range(3)]
        self.test_contacts[0]["tel"]["value"] = "+34111111111"
        map(self.data_layer.insert_contact, self.test_contacts)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.enterNumber("1111")

        suggestion_item = self.UTILS.element.getElement(DOM.Dialer.suggestion_item_single, "Suggestion item")
        self.UTILS.test.test(self.test_contacts[0]["tel"]["value"] in suggestion_item.text,
                        "'{}' is shown as a suggestion".format(self.test_contacts[0]["tel"]["value"]))
