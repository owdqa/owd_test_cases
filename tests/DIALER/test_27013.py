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
        self.UTILS      = UTILS(self)
        self.dialer     = Dialer(self)
        self.contacts   = Contacts(self)

        self.num  = self.UTILS.general.get_config_variable("phone_number", "custom")

        # Remove the phone number from the contact and insert it.
        self.Contact_1 = MockContact(tel={'type': '', 'value': ''})
        self.UTILS.general.insertContact(self.Contact_1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):
        #
        # Add a number and add it to an existing contact.
        #
        self.dialer.launch()
        self.dialer.enterNumber(self.num)
        self.dialer.addThisNumberToContact(self.Contact_1["name"])
 
        #
        # Verify that this contact has been modified in contacts.
        #
        self.apps.kill_all()
        self.contacts.launch()
        self.contacts.view_contact(self.Contact_1["name"])

        x = self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Contact telephone number")
        self.UTILS.test.test(self.num in x.text, "Phone number contains %s (it was %s)." % (self.num, x.text))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Final screenshot and html dump:", x)        