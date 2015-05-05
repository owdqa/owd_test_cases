# OWD 26799:  [DIALER] Make a call by typing a phone number of a contact  
# ** Procedure
#       1- Open dialer app
#       2- Write a contact number 
#       3- Make the call
# ** Expected Results
#       The call is successful and the contact name is shown
from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(SpreadtrumTestCase):

    def setUp(self):
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.dialer = Dialer(self)

        # Get details of our test contacts.
        self.test_contact = MockContact(tel={'type': 'Mobile', 'value': '665666666'})
        self.UTILS.general.insertContact(self.test_contact)

        self._name = self.test_contact["name"]
        self.phone_number = self.test_contact["tel"]["value"]

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()

        self.dialer.enterNumber(self.phone_number)
        self.dialer.call_this_number()

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)

        outgoing_number = self.UTILS.element.getElement(DOM.Dialer.outgoing_call_number, "Outgoing number").text.encode("utf-8")
        self.UTILS.reporting.logResult('info', 'Outgoing number: {}'.format(outgoing_number))
        
        # We use 'in' since it's possible that the displayed outgoing contact name is ellipsed
        self.UTILS.test.test(outgoing_number in self._name, "Outgoing call found with name matches '{}'".format(self._name))
        time.sleep(2)
        self.dialer.hangUp()
