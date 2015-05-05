#===============================================================================
# 26864: Try send a sms to a contact while airplane is enabled (from sms app
# - use contact option)
#
# Procedure:
# 1. Activate Airplane mode
# 2. Open SMS app and click on new message
# 3. Click on Contact button
# ER1
# 4. Select the contact
# ER2
# 5. Write the sms text and click on Send button
# ER3
# 6. Click on Ok button
# ER4
#
# Expected results:
# ER1. The contact app must be openen
# ER2. The sms app must be openen again
# ER3. The app must show a dialog informing that the Flight Safe Mode is active
# ER4. The sms must not be sent and the sms must be shown in the sms thread with
# an X icon on the right.
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(SpreadtrumTestCase):

    test_msg = "Test."

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        # Put the phone into airplane mode.
        self.data_layer.set_setting('airplaneMode.enabled', True)

        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact = MockContact(tel={'type': 'Mobile', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        self.contacts.launch()
        self.contacts.view_contact(self.contact["name"])
        sms_btn = self.UTILS.element.getElement(DOM.Contacts.sms_button, "SMS button")
        sms_btn.tap()

        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        # Create SMS.
        self.messages.enterSMSMsg(self.test_msg)

        # Click send.
        self.messages.sendSMS()
        time.sleep(3)

        # Check that popup appears.
        self.messages.checkAirplaneModeWarning()
