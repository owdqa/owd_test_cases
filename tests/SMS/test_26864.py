from OWDTestToolkit.firec_testcase import FireCTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(FireCTestCase):

    test_msg = "Test."

    def setUp(self):
        #
        # Set up child objects...
        #
        FireCTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        #
        # Put the phone into airplane mode.
        #
        self.UTILS.statusbar.toggleViaStatusBar('airplane')

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact(tel={'type': 'Mobile', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.statusbar.toggleViaStatusBar('airplane')
        self.UTILS.reporting.reportResults()
        FireCTestCase.tearDown(self)

    def test_run(self):

        self.contacts.launch()
        self.contacts.view_contact(self.contact["name"])
        x = self.UTILS.element.getElement(DOM.Contacts.sms_button, "SMS button")
        x.tap()

        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        #
        # Create SMS.
        #
        self.messages.enterSMSMsg(self.test_msg)

        #
        # Click send.
        #
        self.messages.sendSMS(check=False)
        time.sleep(3)

        #
        # Check that popup appears.
        #
        self.messages.checkAirplaneModeWarning()
