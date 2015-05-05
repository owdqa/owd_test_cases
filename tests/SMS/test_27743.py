#===============================================================================
# 27743: Edit a contact name and verify that the SMS list now shows the new name
#
# Procedure:
# 1- Send a sms to our device from phone number who is a contact
# 2- Open SMS app
# ER1
# 3- Edit the contact name who sended the last sms
# 4- Open SMS app
# ER2
#
# Expected results:
# ER1- verify that the SMS list shows the name
# ER2- verify that the SMS list now shows the new name
#===============================================================================

from OWDTestToolkit.spreadtrum_testcase import SpreadtrumTestCase

from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact


class test_main(SpreadtrumTestCase):

    def setUp(self):

        # Set up child objects...
        SpreadtrumTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.messages = Messages(self)
        self.contacts = Contacts(self)

        # Prepare the contact we're going to insert.
        self.phone_number = self.UTILS.general.get_config_variable("phone_number", "custom")
        self.contact_1 = MockContact(tel={'type': '', 'value': self.phone_number})
        self.contact_2 = MockContact(tel={'type': '', 'value': self.phone_number})

        self.UTILS.general.insertContact(self.contact_1)
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact_1["tel"]["value"])

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        SpreadtrumTestCase.tearDown(self)

    def test_run(self):

        # Launch messages app.
        self.messages.launch()
        """
        Send a message to create a thread (use number, not name as this
        avoids some blocking bugs just now).
        """

        self.messages.create_and_send_sms([self.contact_1["tel"]["value"]], "Test message.")
        self.messages.wait_for_message()

        # Open contacts app and modify the contact used to send the SMS in the previous step
        self.contacts.launch()
        self.UTILS.reporting.logComment("Using target telephone number " + self.contact_2["tel"]["value"])
        self.contacts.edit_contact(self.contact_1["name"], self.contact_2)

        # Re-launch messages app.
        self.messages.launch()

        # Verify the thread now contains the name of the contact instead of the phone number
        self.UTILS.reporting.logComment("Trying to open the thread with name: " + self.contact_2["name"])
        self.messages.openThread(self.contact_2["name"])
