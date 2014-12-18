# 26788: Tap in a log entry corresponding to an outgoing call with a test_contact
#        with photo linked to perform a call to this number
# ** Procedure
#
# ** Expected Results
#
import time
from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from OWDTestToolkit.utils.contacts import MockContact


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.test_contact = MockContact(tel={'type': 'Mobile', 'value': "665666666"})

        # Generate an entry in the call log
        self.dialer.launch()
        self.dialer.callLog_clearAll()
        self.dialer.createMultipleCallLogEntries(self.test_contact["tel"]["value"], 1)

        # Create contact with image
        self.UTILS.general.add_file_to_device('./tests/_resources/contact_face.jpg')
        self.dialer.callLog_createContact(self.test_contact["tel"]["value"])

        contFields = self.contacts.get_contact_fields()
        self.contacts.replace_str(contFields['givenName'], self.test_contact["givenName"])
        self.contacts.replace_str(contFields['familyName'], self.test_contact["familyName"])

        self.contacts.add_gallery_image_to_contact(0)
        done_button = self.UTILS.element.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()

        time.sleep(1)
        self.apps.kill_all()
        time.sleep(2)

    def tearDown(self):
        self.UTILS.general.remove_files()
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.dialer.launch()
        self.dialer.open_call_log()

        entry = self.UTILS.element.getElement(("xpath",
                                               DOM.Dialer.call_log_number_xpath.format(self.test_contact["tel"]["value"])),
                                              "The call log for number {}".format(self.test_contact["tel"]["value"]))
        entry.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.element.waitForElements(("xpath", DOM.Dialer.outgoing_call_numberXP.format(self.test_contact["name"])),
                                           "Outgoing call found with number matching {}".format(self.test_contact["name"]))
        time.sleep(2)
        self.dialer.hangUp()
