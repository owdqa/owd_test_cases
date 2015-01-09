import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    test_msg = "Test."

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        self.target_mms_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact_1 = MockContact(tel={'type': 'Mobile', 'value': self.target_mms_number})
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact_1["tel"]["value"])
        self.UTILS.general.insertContact(self.contact_1)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.contacts.launch()
        self.contacts.view_contact(self.contact_1['name'])

        # Tap the sms button in the view details screen to go to the sms page.
        sms_button = self.UTILS.element.getElement(DOM.Contacts.sms_button, "Send SMS button")
        sms_button.tap()

        self.apps.switch_to_displayed_app()
        time.sleep(10)

        self.wait_for_condition(lambda m: m.find_element(*DOM.Messages.target_numbers).text ==
                                self.contact_1['name'], timeout=10, message="To field is already prepulated with our contact info")

        # Create SMS.
        self.messages.enterSMSMsg(self.test_msg)
        self.messages.sendSMS()

        # Wait for the last message in this thread to be a 'received' one.
        self.UTILS.statusbar.wait_for_notification_toaster_detail(self.test_msg, timeout=120)
        self.UTILS.statusbar.click_on_notification_detail(self.test_msg, DOM.Messages.frame_locator)

        self.messages.check_last_message_contents(self.test_msg)
