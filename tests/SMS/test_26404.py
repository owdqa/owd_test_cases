from gaiatest import GaiaTestCase

from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.messages import Messages
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.utils.contacts import MockContact
import time


class test_main(GaiaTestCase):

    def setUp(self):

        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.contacts = Contacts(self)
        self.messages = Messages(self)

        # Prepare the contact we're going to insert.
        self.contact = MockContact()
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):

        # Launch contacts app.
        self.contacts.launch()

        # View the details of our contact.
        self.contacts.view_contact(self.contact['name'])

        # Tap the sms button in the view details screen to go to the sms page.
        smsBTN = self.UTILS.element.getElement(DOM.Contacts.sms_button, "Send SMS button")
        smsBTN.tap()
        """
        Switch to the 'Messages' app frame (or marionette will still be watching the
        'Contacts' app!).
        """

        time.sleep(2)
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        """
        test: this automatically opens the 'send SMS' screen, so
        check the correct name is in the 'to' field of this sms.
        """

        self.messages.checkIsInToField(self.contact['name'])
