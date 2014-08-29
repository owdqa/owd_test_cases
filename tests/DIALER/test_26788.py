# 26788: Tap in a log entry corresponding to an outgoing call with a
# contact with photo linked to perform a call to this number

from gaiatest import GaiaTestCase
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.utils import UTILS
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.dialer import Dialer
from tests._mock_data.contacts import MockContact
import time


class test_main(GaiaTestCase):

    def setUp(self):
        # Set up child objects...
        GaiaTestCase.setUp(self)
        self.UTILS = UTILS(self)
        self.dialer = Dialer(self)
        self.contacts = Contacts(self)

        self.contact = MockContact(tel={'type': 'Mobile', 'value': "665666666"})
        self.UTILS.general.insertContact(self.contact)

    def tearDown(self):
        self.UTILS.reporting.reportResults()
        GaiaTestCase.tearDown(self)

    def test_run(self):
        self.UTILS.general.addFileToDevice('./tests/_resources/contact_face.jpg', destination='DCIM/100MZLLA')

        self.dialer.launch()
        self.dialer.callLog_clearAll()

        self.dialer.enterNumber(self.contact["tel"]["value"])
        self.dialer.callThisNumber()
        time.sleep(2)

        self.dialer.hangUp()
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

        self.dialer.openCallLog()

        x = self.UTILS.element.getElement(("xpath",
                                           DOM.Dialer.call_log_number_xpath.format(self.contact["tel"]["value"])),
                                          "The call log for number {}".format(self.contact["tel"]["value"]))
        x.tap()

        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot of call_log entry", screenshot)
        time.sleep(2)
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.call_log_contact_name_iframe, via_root_frame=False)

        x = self.UTILS.element.getElement(DOM.Contacts.view_contact_tel_field, "Telephone field")
        x.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)

        self.UTILS.element.waitForElements(("xpath", DOM.Dialer.outgoing_call_numberXP.format(self.contact["name"])),
                                           "Outgoing call found with number matching {}".format(self.contact["name"]))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot of dialer", x)

        time.sleep(2)
        self.dialer.hangUp()
